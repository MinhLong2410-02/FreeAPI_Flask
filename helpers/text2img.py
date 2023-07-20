import os, json, requests
import dotenv
dotenv.load_dotenv("./.env")
def draw(prompt, model_id, height=None, width=None):
    url = os.environ['TEXT2IMG_URL']
    
    height = 512 if height is None else height
    width = 512 if width is None else width

    payload = json.dumps({
        "key": os.environ['KEY'],
        "model_id": model_id,
        "prompt": prompt,
        "negative_prompt":
        "(low quality, worst quality:1.4), (bad anatomy), (inaccurate limb:1.2),bad composition, inaccurate eyes, extra digit,fewer digits,(extra arms:1.2), EasyNegative",
        "height": str(height),
        "width": width,
        "samples": 1,
        "num_inference_steps": 80,
        "safety_checker": "yes",
        "enhance_prompt": "yes",
        "seed": 3259750601,
        "guidance_scale": 7,
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "yes",
        "embeddings": 'embeddings_models_id',
        "lora": 'lora_model_id',
        "webhook": None,
        "track_id": None,
    })
    headers = {"Content-Type": "application/json"}
    # while True:
    #     data = requests.request("POST", url, headers=headers,
    #                             data=payload).json()
    #     if data['status'] == 'success':
    #         break
    data = requests.request("POST", url, headers=headers, data=payload).json()
    print(data)
    res = {}
    res['status'] = 'success'
    res['generationTime'] = data['generationTime']
    res['prompt'] = data['meta']['prompt']
    res['image_url'] = data['output'][0]
    return res