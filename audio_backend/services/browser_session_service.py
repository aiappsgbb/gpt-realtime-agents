"""Browser-facing session orchestration helpers with Zero Trust authentication."""

from __future__ import annotations

import uuid
import logging
from dataclasses import dataclass
from typing import Dict, Literal

import httpx

from common.config import (
    BrowserRealtimeConfig,
    VoiceLiveConfig,
    get_browser_realtime_config,
    get_voice_live_config,
)

logger = logging.getLogger(__name__)

ConnectionMode = Literal["webrtc", "voice-live"]


@dataclass(frozen=True)
class BrowserSession:
    session_id: str
    ephemeral_key: str | None  # Optional for managed identity authentication
    realtime_url: str
    deployment: str
    voice: str


def _ensure_headers(headers: Dict[str, str] | None) -> Dict[str, str]:
    if not headers:
        raise RuntimeError("Auth headers must be provided for realtime session requests")
    return headers


async def create_browser_session(
    *,
    connection_mode: ConnectionMode,
    deployment: str,
    voice: str,
    realtime_headers: Dict[str, str] | None,
) -> BrowserSession:
    """Create a session for the requested browser connection mode using Zero Trust authentication."""

    logger.info("[create_browser_session] connection_mode=%s, deployment=%s, voice=%s", 
                connection_mode, deployment, voice)
    if connection_mode  == "webrtc":
        return await _create_gpt_realtime_session(
            deployment=deployment,
            voice=voice,
            headers=_ensure_headers(realtime_headers),
        )

    if connection_mode == "voice-live":
        return _create_voice_live_session(deployment=deployment, voice=voice)

    raise ValueError(f"Unsupported connection mode: {connection_mode}")



async def _create_gpt_realtime_session(
    *, deployment: str, voice: str, headers: Dict[str, str]
) -> BrowserSession:
    config: BrowserRealtimeConfig = get_browser_realtime_config()
    payload = {"model": deployment, "voice": voice}

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            config.realtime_session_url,
            headers=headers,
            json=payload,
        )
        response.raise_for_status()

    data = response.json()
    ephemeral_key = data.get("client_secret", {}).get("value")
    session_id = data.get("id")
    if not ephemeral_key or not session_id:
        raise RuntimeError("Malformed session response from Azure Realtime API")

    return BrowserSession(
        session_id=session_id,
        ephemeral_key=ephemeral_key,
        realtime_url=config.webrtc_url,
        deployment=deployment or config.default_deployment,
        voice=voice or config.default_voice,
    )


def _create_voice_live_session(*, deployment: str, voice: str) -> BrowserSession:
    """Create a Voice Live session.
    
    Note: Voice Live mode requires managed identity authentication configured.
    This function creates a session using the endpoint URL only.
    """
    config: VoiceLiveConfig = get_voice_live_config()
    model = deployment or config.default_model

    url = f"{config.endpoint}/voice-live/realtime?api-version=2025-05-01-preview&model={model}"
    url = url.replace("https://", "wss://")

    # Voice Live requires managed identity - ephemeral key will be obtained through Azure AD auth
    # Generate a unique session ID for tracking
    return BrowserSession(
        session_id=str(uuid.uuid4()),
        ephemeral_key=None,  # No API key - uses managed identity token
        realtime_url=url,
        deployment=model or config.default_model,
        voice=voice or config.default_voice,
    )
