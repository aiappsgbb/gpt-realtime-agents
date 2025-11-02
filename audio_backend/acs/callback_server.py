import sys
from pathlib import Path
print(f"Sys importing {str(Path(__file__).parent )}")
sys.path.insert(0, str(Path(__file__).parent ))

from typing import Dict, Any
from aiohttp import web

from rich.traceback import install
from rich.console import Console
console = Console()

EVENT_GRID_VALIDATION_EVENT_TYPE = "Microsoft.EventGrid.SubscriptionValidationEvent"



class EventHandler:

    def __init__(self, caller):
        self.caller = caller



    async def handle_participants_updated(self, event: Dict[str, Any]):
        """Handle participant changes in the call"""
        try:
            data = event.get("data") or {}
            call_connection_id = data.get("callConnectionId")
            participants = data.get("participants", [])

            console.log(
                f"Participants updated for call {call_connection_id}. Count: [bold]{len(participants)}[/bold]"
            )

            for participant in participants:
                identifier = participant.get("identifier") if isinstance(participant, dict) else participant
                console.log(f"    participant -> {identifier}")

        except Exception as e:
            console.log(f"[bold red]Error handling participants updated[/bold red]: {e}")
            console.print_exception()

    async def callback_events_handler(self, request):

        try:
            events_data = await request.json()

            if isinstance(events_data, dict):
                events = [events_data]
            else:
                events = events_data or []

            for event in events:
                if not isinstance(event, dict):
                    console.log(f"[bold yellow]Skipping unsupported event payload[/bold yellow]: {event}")
                    continue

                event_type = (event.get("type") or event.get("eventType") or "").strip()
                console.log(f"[bold cyan]Processing event[/bold cyan]: {event_type}")

                if event_type == EVENT_GRID_VALIDATION_EVENT_TYPE:
                    data = event.get("data") or {}
                    validation_code = data.get("validationCode")
                    validation_url = data.get("validationUrl")

                    if validation_url and not validation_code:
                        console.log(
                            "[bold yellow]Validation URL received but validation code missing. Manual validation may be required.[/bold yellow]"
                        )

                    if validation_code:
                        console.log(
                            f"[bold green]Responding to Event Grid validation with code[/bold green]: {validation_code}"
                        )
                        return web.Response(status=200, body={"validationResponse": validation_code})

                    console.log("[bold red]Validation event missing code; continuing processing[/bold red]")
                    continue

                if event_type == "Microsoft.Communication.IncomingCall":
                    print(f"Incoming call event data: {event}")
                    await self.caller.inbound_call_handler(event)
                elif event_type == "Microsoft.Communication.CallConnected":
                    await self.caller.call_connected_handler(event)
                elif event_type == "Microsoft.Communication.ParticipantsUpdated":
                    await self.handle_participants_updated(event)
                elif event_type == "Microsoft.Communication.CallDisconnected":
                    await self.caller.call_disconnected_handler(event)
                else:
                    console.log(f"Unhandled event type: {event_type}\n{event}")

            return web.Response(status=200)

        except Exception as e:
            console.log(f"[bold red]Error processing callback request[/bold red]: {e}")
            console.print_exception()
            return {"error": "Internal server error processing callbacks"}

