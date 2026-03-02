from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.templating import Jinja2Templates
from app.hotels.routers import get_all_hotels, get_hotels_by_location

router = APIRouter(prefix='/pages', tags=['frontend'])
templating = Jinja2Templates('app/templates')

@router.get('/hotels')
async def get_hotels_page(request: Request,
                          hotels = Depends(get_hotels_by_location)):
    return  templating.TemplateResponse(name='hotels.html',
                                        context={'request': request, 'hotels': hotels})
