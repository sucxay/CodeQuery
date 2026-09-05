from pydantic import BaseModel

class requestURL(BaseModel):
    github_url:str

class askQuestion(BaseModel):
    question:str

    
