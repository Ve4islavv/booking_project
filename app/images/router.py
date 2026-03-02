from fastapi import APIRouter, UploadFile
import shutil


router = APIRouter(prefix='/images',
                   tags=['загрузка картинок'])


@router.post('/hotels')
async def add_image(name: int,
                    file: UploadFile):
   with open(f'app/static/images/{name}.webp', 'wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)