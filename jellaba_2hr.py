import gradio as gr
from controlnet_aux import OpenposeDetector
from PIL import Image
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
import torch
from controlnet_aux import OpenposeDetector
from diffusers.utils import load_image

#Models
openpose = OpenposeDetector.from_pretrained('lllyasviel/ControlNet')
controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-openpose", torch_dtype=torch.float16)
pipe = StableDiffusionControlNetPipeline.from_pretrained("helkoo/jelaba_2HR", controlnet=controlnet, safety_checker=None, torch_dtype=torch.float16)

#optimizations
pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
#pipe.enable_xformers_memory_efficient_attention()
#pipe.enable_model_cpu_offload()
pipe = pipe.to("cuda")

def generate(image,prompt):
    image = openpose(image)
    #image = image
    image = pipe(prompt, image, num_inference_steps=20).images[0]
    return image

gr.Interface(fn=generate, inputs=["image","text"], outputs="image").launch(share=True, debug=True)

import numpy as np
import requests
def generate2(prompt,taille):
    if taille == "S":
      image = Image.open(requests.get('https://mode-et-caftan.com/757-large_default/jellaba-salsa-marocaine-femme.jpg', stream=True).raw)

    if taille == "XL":
      image = Image.open(requests.get('https://i.pinimg.com/236x/03/f1/36/03f136b83bb37c9f17c3764f1b36f9fa--big-is-beautiful-curvy-fashion.jpg', stream=True).raw)
    
    if taille == "L":
      image = Image.open(requests.get('https://mode-et-caftan.com/757-large_default/jellaba-salsa-marocaine-femme.jpg', stream=True).raw)

    # convert image to numpy array
    image = np.array(image)
    image = openpose(image)
    #image = image
    image = pipe(prompt, image, num_inference_steps=20).images[0]
    return image

gr.Interface(fn=generate2, inputs=["text",
                                   gr.Dropdown(
                                  ["S", "L", "XL"], label="taille", info="choisie la taille"
        ),
        ], outputs="image").launch(share=True, debug=True)

