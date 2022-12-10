from django import forms
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    
    CITY = [
        ['台北市', '台北市'],
        ['桃園市', '桃園市'],
        ['台中市', '台中市'],
        ['嘉義市', '嘉義市'],
        ['嘉義縣', '嘉義縣'],
        ['台南市', '台南市'],
        ['高雄市', '高雄市'],
        ['屏東縣', '屏東縣'],
        ['其他', '其他'],
    ]
    user_name = forms.CharField(label='您的名字', max_length=50)
    user_city = forms.ChoiceField(label='居住城市', choices=CITY)
    user_email = forms.EmailField(label='電子信箱', max_length=50)
    user_phone = forms.CharField(label='您的電話', max_length=12)
    user_msg = forms.CharField(label='您的意見', widget=forms.Textarea)
    captcha = CaptchaField(label='驗證碼')