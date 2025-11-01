import os
from PIL import Image
from src.tasks.celery_app import celery_app 


@celery_app.task
def resize_image(image_path: str):
    sizes = [1000, 500, 200]



    img = Image.open(image_path)

    
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    
    for size in sizes:
        output_folder = 'src/static/img/'
        if size == 1000:
            output_folder += "1000px"
        elif size == 500: 
            output_folder += "500px"
        else:
            output_folder += "200px"

        
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)

        
        new_file_name = f"{name}_{size}px{ext}"

        
        output_path = os.path.join(output_folder, new_file_name)
        print(output_path)
        
        img_resized.save(output_path)

    print(f"Изображение сохранено в следующих размерах: {sizes}")