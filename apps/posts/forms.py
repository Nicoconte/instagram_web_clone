from django import forms

class PostForm(forms.Form):
    description = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            "class" : "form-control mt-2",
            "placeholder" : "Escribe un pie de foto o video"
        }
    ))

    files = forms.FileField(label="", widget=forms.ClearableFileInput(
        attrs={
            "class" : "form-control mt-3", 
            "multiple" : True
        }
    ))

