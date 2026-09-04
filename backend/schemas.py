from pydantic import BaseModel


class RepositoryRequest(BaseModel):
    github_url: str


class QuestionRequest(BaseModel):
    question: str