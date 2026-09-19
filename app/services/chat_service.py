from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.booking import BookingCreate
from app.services.booking_service import booking_service
from app.services.llm_service import llm_service
from app.services.memory_service import memory_service
from app.services.retriever_service import retriever_service

class ChatService:

    async def chat(
        self,
        session: AsyncSession,
        session_id: str,
        user_message: str,
    ) -> str:   
        existing_booking_id = await memory_service.get_booking_id(
            session_id=session_id,
        )

        if existing_booking_id is not None:
            assistant_response = (
                "Your interview has already been booked successfully. "
                f"Your booking ID is {existing_booking_id}."
            )

            await memory_service.add_message(
                session_id=session_id,
                role="user",
                content=user_message,
            )

            await memory_service.add_message(
                session_id=session_id,
                role="assistant",
                content=assistant_response,
            )

            return assistant_response

        await memory_service.add_message(
            session_id=session_id,
            role="user",
            content=user_message,
        )
    
        history = await memory_service.get_messages(
            session_id=session_id,
        )
       
        booking_started = await memory_service.is_booking_started(
            session_id=session_id,
        )

        booking_keywords = (
            "book an interview",
            "book interview",
            "schedule an interview",
            "schedule interview",
            "want to book",
            "want to schedule",
            "book my interview",
            "schedule my interview",
        )

        if not booking_started and any(
            keyword in user_message.lower()
            for keyword in booking_keywords
        ):
            await memory_service.set_booking_started(
                session_id=session_id,
            )

            booking_started = True

        retrieved_documents = retriever_service.retrieve(
            query=user_message,
        )

        retrieved_context = "\n".join(
            retrieved_documents
        )

        if not retrieved_context:
            retrieved_context = (
                "No relevant information was found "
                "in the knowledge base."
            )

        system_prompt = (
            "You are an interview booking assistant.\n\n"
            "Answer general interview questions using the "
            "knowledge base.\n\n"
            "If the user wants to book an interview, collect "
            "these four pieces of information:\n"
            "1. Full name\n"
            "2. Email address\n"
            "3. Interview date\n"
            "4. Interview time\n\n"
            "Ask only for the next missing piece of information.\n"
            "Do not ask unnecessary questions.\n"
            "Do not invent information.\n"
            "Keep responses short and conversational.\n\n"
            "Relevant knowledge base information:\n"
            f"{retrieved_context}"
        )

        messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": system_prompt,
            },
            *history,
        ]

        assistant_response = await llm_service.generate_response(
            messages=messages,
        )

        if booking_started:
            booking = await llm_service.extract_booking(
                messages=history,
            )

            if (
                booking.name is not None
                and booking.email is not None
                and booking.date is not None
                and booking.time is not None
            ):
                booking_data = BookingCreate(
                    name=booking.name,
                    email=booking.email,
                    date=booking.date,
                    time=booking.time,
                )

                saved_booking = (
                    await booking_service.create_booking(
                        session=session,
                        booking_data=booking_data,
                    )
                )

                await memory_service.set_booking_id(
                    session_id=session_id,
                    booking_id=saved_booking.id,
                )

                assistant_response = (
                    "Your interview has been booked successfully. "
                )

        await memory_service.add_message(
            session_id=session_id,
            role="assistant",
            content=assistant_response,
        )

        return assistant_response

chat_service = ChatService()