import re

class RetrieverService:

    def __init__(self) -> None:
        self.documents: list[str] = [
            (
                "Interview duration: The interview usually takes "
                "approximately 45 minutes."
            ),
            (
                "Interview location: Interviews are conducted "
                "online through a video meeting."
            ),
            (
                "Required documents: Candidates should keep their "
                "resume and a valid identification document ready."
            ),
            (
                "Interview preparation: Candidates should review "
                "their experience, skills, and previous projects."
            ),
            (
                "Interview rescheduling: Candidates should contact "
                "the interview team if they need to change their "
                "scheduled interview time."
            ),
        ]

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[str]:

        query_words = set(
            re.findall(
                r"\b\w+\b",
                query.lower(),
            )
        )

        scored_documents: list[tuple[int, str]] = []

        for document in self.documents:
            document_words = set(
                re.findall(
                    r"\b\w+\b",
                    document.lower(),
                )
            )

            score = len(
                query_words.intersection(document_words)
            )

            if score > 0:
                scored_documents.append(
                    (score, document)
                )

        scored_documents.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            document
            for _, document in scored_documents[:top_k]
        ]
import re


class RetrieverService:

    def __init__(self) -> None:
        self.documents: list[str] = [
            (
                "Interview duration: The interview usually takes "
                "approximately 45 minutes."
            ),
            (
                "Interview location: Interviews are conducted "
                "online through a video meeting."
            ),
            (
                "Required documents: Candidates should keep their "
                "resume and a valid identification document ready."
            ),
            (
                "Interview preparation: Candidates should review "
                "their experience, skills, and previous projects."
            ),
            (
                "Interview rescheduling: Candidates should contact "
                "the interview team if they need to change their "
                "scheduled interview time."
            ),
        ]

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[str]:

        query_words = set(
            re.findall(
                r"\b\w+\b",
                query.lower(),
            )
        )

        scored_documents: list[tuple[int, str]] = []

        for document in self.documents:
            document_words = set(
                re.findall(
                    r"\b\w+\b",
                    document.lower(),
                )
            )

            score = len(
                query_words.intersection(document_words)
            )

            if score > 0:
                scored_documents.append(
                    (score, document)
                )

        scored_documents.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            document
            for _, document in scored_documents[:top_k]
        ]

retriever_service = RetrieverService()
