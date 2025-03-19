from django.shortcuts import render,redirect
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
from django.core.files.storage import default_storage
from django.conf import settings
import os
import pickle
import numpy as np
from django.contrib.auth import logout
from .models import *
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):
    return render(request,"farmer/index.html")


def about(request):
    return render(request,"farmer/about.html")


def adminlogin(request):
    if request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password")

        if name == "admin" and password == "admin":
            messages.success(request,"Login Successfull !")
            print("success")
            return redirect("admin_dashboard")
        else:
            messages.error(request,"Invalid Details !")
            print("Invalid Details")
            return redirect("adminlogin")
    return render(request,"farmer/admin-login.html")


def farmerregister(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        location = request.POST.get('address')
        profile = request.FILES.get('profile')
        try:
            User.objects.get(user_email = email)
            messages.info(request, 'Email Already Exists!')
            return redirect('farmerregister')
        except:
            user = User.objects.create(user_name=name, user_email=email, user_phone=phone, user_profile=profile, user_password=password, user_location=location)
            print(user)
            messages.success(request, 'Account Created Successfully!')
            return redirect('farmerregister')
    return render(request,"farmer/farmer-register.html")


def farmerlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(user_email=email)   
            if user.user_password == password:
                if user.status == 'Accepted':
                    request.session['user_id'] = user.user_id
                    messages.success(request, 'Login Successful')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Your account is not approved yet.')
                    return redirect('farmerlogin')
            else:
                messages.error(request, 'Incorrect Password')
                return redirect('farmerlogin')
        except User.DoesNotExist:
            messages.error(request, 'Invalid Login Details')
            return redirect('farmerlogin')
    return render(request,"farmer/farmer-login.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            messages.success(request, 'Login Successful')
            return redirect('govt_dashboard')
        else:
            messages.error(request, 'Invalid details !')
            return redirect('govtlogin')
    return render(request,"farmer/govtofficer-login.html")



def expertlogin(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            messages.success(request, 'Login Successful')
            return redirect('expert_dashboard')
        else:
            messages.error(request, 'Invalid details !')
            return redirect('expertlogin')
    return render(request,"farmer/experts.html")



def contact(request):
    return render(request,"farmer/contact.html")

# views.py
from django.shortcuts import render
from .models import CropPrediction



def dashboard(request):
    predictions = CropPrediction.objects.all()  # Get all CropPrediction objects

    return render(request,"farmer/farmer-dashboard.html" , {'predictions': predictions})


def profile(request):
    user_id  = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            profile = request.FILES['profile']
            user.user_profile = profile
        except MultiValueDictKeyError:
            profile = user.user_profile
        password = request.POST.get('password')
        location = request.POST.get('location')
        user.user_name = name
        user.user_email = email
        user.user_phone = phone
        user.user_password = password
        user.user_location = location
        user.save()
        messages.success(request , 'updated succesfully!')
        return redirect('profile')
    return render(request,"farmer/myprofile.html",{'i':user})




def feedback(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = User.objects.filter(user_id=user_id).first()

        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        rating = request.POST.get('rating')
        additional_comments = request.POST.get('additional_comments')

        feedback_instance = Feedback.objects.create(
            user=user,
            user_name=user_name,
            user_email=user_email,
            rating=rating,
            additional_comments=additional_comments
        )
        feedback_instance.save()
        messages.success(request,"Feedback Submitted Successfully !")
        return redirect('farmer_feedback')

    return render(request,"farmer/farmer-feedback.html")

def user_logout(request):
    logout(request)
    return redirect('farmerlogin')



import re
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Conversation
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatbot(request):
    conversations = Conversation.objects.all().order_by('created_at')
    
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        if user_message:
            # Call Perplexity API
            headers = {
                "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "sonar",
                "messages": [
                    {
                        "role": "system",
                        "content": "Be precise and concise."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
            
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                json=payload,
                headers=headers
            )
            
            bot_response = "Error: Could not get response from AI"
            if response.status_code == 200:
                try:
                    bot_response = response.json()['choices'][0]['message']['content']
                    
                    # Remove markdown bold () and any references (e.g., [1], [2], etc.)
                    bot_response = re.sub(r'\\([^]+)\\*', r'\1', bot_response)  # Remove bold
                    bot_response = re.sub(r'\[\d+\]', '', bot_response)  # Remove reference numbers
                except:
                    pass
                
            Conversation.objects.create(
                user_message=user_message,
                bot_response=bot_response
            )
            
            return redirect('chatbot')
    
    return render(request, 'farmer/chatbot.html', {'conversations': conversations})




model = load_model('model_inception.h5')

ref = {
    0: 'Pepper__bell___Bacterial_spot',
    1: 'Pepper__bell___healthy',
    2: 'Potato___Early_blight',
    3: 'Potato___Late_blight',
    4: 'Potato___healthy',
    5: 'Tomato - Bacterial_spot',
    6: 'Tomato - Early_blight',
    7: 'Tomato - Healthy',
    8: 'Tomato - Late_blight',
    9: 'Tomato - Leaf_Mold',
    10: 'Tomato - Septoria_leaf_spot',
    11: 'Tomato - Target_Spot',
    12: 'Tomato - Tomato_Yellow_Leaf_Curl_Virus',
    13: 'Tomato - Tomato_mosaic_virus',
    14: 'Tomato - Two-spotted_spider_mite',
    15: 'diseased cotton leaf',
    16: 'diseased cotton plant',
    17: 'fresh cotton leaf',
    18: 'fresh cotton plant',
    19: 'Apple___Apple_scab',
    20: 'Apple___Black_rot',
    21: 'Apple___Cedar_apple_rust',
    22: 'Apple___healthy',
    23: 'Blueberry___healthy',
    24: 'Cherry_(including_sour)___Powdery_mildew',
    25: 'Cherry_(including_sour)___healthy',
    26: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    27: 'Corn_(maize)___Common_rust_',
    28: 'Corn_(maize)___Northern_Leaf_Blight',
    29: 'Corn_(maize)___healthy',
    30: 'Grape___Black_rot',
    31: 'Grape___Esca_(Black_Measles)',
    32: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    33: 'Grape___healthy',
    34: 'Orange___Haunglongbing_(Citrus_greening)',
    35: 'Peach___Bacterial_spot',
    36: 'Peach___healthy',
    37: 'Raspberry___healthy',
    38: 'Soybean___healthy'
}




from django.shortcuts import render
from django.contrib import messages
from .models import User, CropPrediction
from django.core.files.storage import default_storage
from django.conf import settings
from django.http import JsonResponse

def prediction(path):
    img = image.load_img(path, target_size=(224, 224))
    i = image.img_to_array(img)
    i = np.expand_dims(i, axis=0)
    img = preprocess_input(i)
    pred = np.argmax(model.predict(img), axis=1)
    crop_name = ref[pred[0]]  # Get the name of the predicted crop

    # Sample generic suggestions for demonstration
    generic_suggestions = {
        'how_to_grow': [
            "Plant in well-drained, fertile soil.",
            "Ensure proper sunlight exposure for at least 6-8 hours a day.",
            "Maintain adequate spacing to allow for healthy growth."
        ],
        'care': [
            "Water regularly but avoid overwatering to prevent root rot.",
            "Mulch the soil to retain moisture and prevent weed growth.",
            "Ensure proper pest management by inspecting leaves and stems regularly."
        ],
        'pesticides': [
            "Use neem oil for natural pest control.",
            "Apply insecticidal soap for soft-bodied pests.",
            "Consider using a systemic insecticide for long-term protection."
        ]
    }

    return crop_name, generic_suggestions

from django.shortcuts import render
from django.contrib import messages
from .models import User, CropPrediction
from django.core.files.storage import default_storage
from django.conf import settings
from googletrans import Translator

translator = Translator()

def translate_text(text, target_lang):
    """Translate text to the target language."""
    try:
        return translator.translate(text, dest=target_lang).text
    except Exception as e:
        return text  # Return original if translation fails

def cropdisease(request):
    result = ""
    growth_tips = []
    care_tips = []
    pesticide_suggestions = []
    translated_result = ""
    
    if request.method == "POST" and 'image' in request.FILES:
        uploaded_image = request.FILES['image']
        file_path = default_storage.save(uploaded_image.name, uploaded_image)
        path = settings.MEDIA_ROOT + '/' + file_path

        user_id = request.session.get('user_id')
        user = User.objects.filter(user_id=user_id).first()

        result, crop_suggestions = prediction(path)

        growth_tips = crop_suggestions.get('how_to_grow', [])
        care_tips = crop_suggestions.get('care', [])
        pesticide_suggestions = crop_suggestions.get('pesticides', [])

        # Default translation to Hindi (Can be changed dynamically)
        translated_result = translate_text(result, 'hi')

        crop_prediction = CropPrediction(
            user=user,
            uploaded_image=uploaded_image,
            plant_type=result,
            growth_tips="\n".join(growth_tips),
            care_tips="\n".join(care_tips),
            pesticide_suggestions="\n".join(pesticide_suggestions)
        )
        crop_prediction.save()

        messages.success(request, "Detection Completed!")
        return render(request, "farmer/cropdisease.html", {
            'result': result,
            'translated_result': translated_result,  # Pass translated result to the template
            'growth_tips': growth_tips,
            'care_tips': care_tips,
            'pesticide_suggestions': pesticide_suggestions
        })

    return render(request, "farmer/cropdisease.html")
