# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 05:28:02 2024

@author: rezer
"""
from PIL import PngImagePlugin
prefix_prompts="1girl,"

suffix_prompts=",masterpiece,best quality,absurdres,newest," #质量词

neg_prompts="bad anatomy,blurry,(worst quality:1.8),low quality,hands bad,face bad,(normal quality:1.3),bad hands,mutated hands and fingers,extra legs,extra arms,duplicate,cropped,text,jpeg,artifacts,signature,watermark,username,blurry,artist name,trademark,title,multiple view,Reference sheet,long body,multiple breasts,mutated,bad anatomy,disfigured,bad proportions,duplicate,bad feet,artist name,ugly,text font ui,missing limb,monochrome,"
def gen_tag(lora_name:str,core_tag:str):
    lora_prompt=f"<lora:{lora_name}:1>"
    #core tag:
    full_body_words="full body"
    portrait_words="portrait,looking at viewer"
    profile_words="profile,from side,upper body"
    base_words=""
    # f"{prefix_prompts},{core_tag},{lora_prompt}"
    #skins:
        
    shorts_word="bandeau,belt,coat,cowboy shot,looking at viewer,midriff,navel,open clothes,open coat,short shorts,shorts,smile,standing,stomach,strapless,long sleeves,tube top,wide sleeves,:d,crop top,open mouth,hand on hip,hand up,simple background,thighs,cleavage,jacket"

    china_dress_word="bare shoulders,bead bracelet,beads,china dress,chinese clothes,dress,jewelry,looking at viewer,sleeveless,sleeveless dress,solo,bracelet,smile,medium breasts,thighs,cowboy shot,:d,open mouth"

    bikini_words="bikini,night, starry sky, beach,standing,looking at viewer,light smile"
    maid_words="maid, long maid dress"
    yukata_words="yukata,kimono"
    miko_words="white kimono,red hakama,wide sleeves"
    suit_words="black business suit, tie, sunglasses, white gloves, white shirt, black skirt, smoking, handsome"
    
    
    nude1_words="lying on bed,nude, spread legs, arms up, mature, nipples, pussy, pussy juice, looking at viewer, embarrassed, endured face,feet out of frame"
    nude_stand_words="standing, nude, completely nude, mature, nipples, pussy, pussy juice, looking at viewer, embarrassed"

    
    #动作
    sitting_words="sitting,sitting on chair,chair,cowboy shot,looking at viewer"
    squat_words="squatting,cowboy shot,looking at viewer"
    kneel_words="kneeling,kneeling on one knee,on one knee,cowboy shot,looking at viewer"
    jumping_words="jumping,cowboy shot,looking at viewer"
    crossed_arms_words="crossed arms,cowboy shot,looking at viewer"
    
    #表情
    angry_words="angry,annoyed,portrait,looking at viewer"
    smile_words="smile,happy,one eye closed,portrait,looking at viewer"
    cry_words="crying,sobbing,tears,portrait,looking at viewer"
    grin_words="evil grin,evil smile,grin,portrait,looking at viewer"
    
    #sex
    sex_words="1boy, 1girl, shy, embarrassed, pussy, penis, sex, nude, complete nude, breasts, nipples, vagina, clitoris, pussy juice, cum in pussy"
    
    
    num_count=[      
        [portrait_words,3,"portrait_words"],
        [full_body_words,2,"full_body_words"],
        [profile_words,2,"profile_words"],
        [base_words,2,"base_words"],
        
        
        [shorts_word,1,"shorts_word"],
        [china_dress_word,1,'china_dress_word'],
        [bikini_words,3,"bikini_words"],
        [maid_words,2,"maid_words"],
        [yukata_words,1,"yukata_words"],
        [miko_words,1,"miko_words"],
        [suit_words,1,"suit_words"],
        
        [sitting_words,1,"sitting_words"],
        [squat_words,1,"squat_words"],
        [kneel_words,1,"kneel_words"],
        [jumping_words,1,"jumping_words"],
        [crossed_arms_words,1,"crossed_arms_words"],
        
        [angry_words,1,"angry_words"],
        [smile_words,1,"smile_words"],
        [cry_words,1,"cry_words"],
        [grin_words,1,"grin_words"],
        
        [nude1_words,2,"nude1_words"],
        [nude_stand_words,3,"nude_stand_words"],
        [sex_words,2,"sex_words"]
        
        ]
    run_prompts_list=[]
    for run_prompt in num_count:
        prompt= f"{prefix_prompts},{core_tag},{run_prompt[0]},{suffix_prompts}{lora_prompt}"
        for i in range(run_prompt[1]):

            run_prompts_list.append( {"prompt":prompt,
                                      "seed":42+i,
                                      "filename":f"{run_prompt[-1]}_{42+i}"
                                          })
 
    return run_prompts_list
    # print(len(run_prompts_list))

def gen_test_image(api,prompt:str,seed:int,save_file_path:str,):
    bs=1
    result=api.txt2img(
            prompt=prompt,
            negative_prompt=neg_prompts,
            seed=seed,
            cfg_scale=5,
            steps=28,
            batch_size=bs,
            width=960,
            height=1280,
            
            sampler_name="DPM++ 2M Karras"
            
            )
    for i in range(bs):
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", result.info['infotexts'][i])
        result.images[i].save(save_file_path,"PNG", pnginfo=pnginfo)
        
 
