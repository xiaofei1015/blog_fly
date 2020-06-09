from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    # content = forms.CharField(widget=CKEditorWidget(), label='正文', required=True)
    #  上传图片
    content = forms.CharField(
        widget=CKEditorUploadingWidget, label='正文', required=True
    )