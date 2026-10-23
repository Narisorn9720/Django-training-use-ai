# เรียน Django แบบลงมือทำ: จากเริ่มต้นถึงระดับกลาง

คู่มือนี้พาทำความเข้าใจ Django โดยใช้ Todo application ใน repository นี้เป็นโปรเจกต์ฝึก ผู้เรียนจะเห็นทั้งภาพรวมและตัวอย่างโค้ดระดับไฟล์ พร้อมคำอธิบายว่าไฟล์แต่ละส่วนทำหน้าที่อะไรและเชื่อมกันอย่างไร

**เหมาะสำหรับ:** ผู้ที่เขียน Python เบื้องต้นได้ แต่ยังไม่เคยสร้างเว็บด้วย Django

**หลังเรียนจบ คุณจะทำได้:** สร้าง model และ migration, รับข้อมูลจากฟอร์ม, ทำ CRUD, ค้นหาและกรอง, ใช้ template inheritance, ป้องกันฟอร์มด้วย CSRF, จัดการ static files และเขียนแบบทดสอบเริ่มต้น

---

## บทที่ 0: เตรียมโปรเจกต์และรู้จักคำสั่ง

### Django คืออะไร

Django เป็น web framework สำหรับ Python ที่ช่วยจัดการงานพื้นฐานของเว็บ เช่น routing, database, form validation, HTML templates, security และ admin site โดยไม่ต้องเขียนระบบเหล่านี้ขึ้นเองทั้งหมด

คำศัพท์ที่จะใช้ตลอดคู่มือ:

- **Project** คือการตั้งค่าและการเชื่อมแอปต่าง ๆ ของเว็บไซต์ ในโปรเจกต์นี้อยู่ใน `core/`
- **App** คือกลุ่มความสามารถหนึ่งชุด โปรเจกต์นี้มีแอป `todo/`
- **Model** คือคำอธิบายข้อมูลที่ต้องเก็บในฐานข้อมูล
- **View** คือ Python function ที่รับ request แล้วเลือกว่าจะอ่านหรือเปลี่ยนข้อมูลและส่ง response แบบใดกลับไป
- **Template** คือ HTML ที่แสดงข้อมูลจาก view
- **URL pattern** คือกฎจับคู่ URL กับ view
- **Migration** คือไฟล์บันทึกการเปลี่ยนโครงสร้างตารางตาม model

### โครงสร้างโปรเจกต์นี้

```text
django-training-use-ai/
├── manage.py
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── todo/
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    ├── templates/
    │   ├── base.html
    │   └── todo/
    │       ├── confirm_delete.html
    │       ├── create.html
    │       ├── edit.html
    │       └── todo_list.html
    └── static/todo/css/main.css
```

`core/settings.py` ระบุว่าใช้ SQLite ที่ `db.sqlite3`, เปิดใช้งานแอป `todo` และค้นหา template ภายในโฟลเดอร์ templates ของแต่ละ app ด้วย `APP_DIRS=True` (`todo/templates/base.html` จึงใช้ได้)

### เริ่มรันแอป

เปิด Terminal ที่โฟลเดอร์โปรเจกต์ แล้วใช้คำสั่ง:

```bash
python3 manage.py check
python3 manage.py migrate
python3 manage.py runserver
```

เปิด `http://127.0.0.1:8000/` ใน browser

- `check` ตรวจสอบการตั้งค่า Django เบื้องต้น
- `migrate` สร้าง/ปรับตาราง SQLite ตาม migration ที่มีอยู่
- `runserver` เปิดเว็บเซิร์ฟเวอร์สำหรับพัฒนา กด `Ctrl+C` เพื่อหยุด
- `python3 manage.py help` แสดงคำสั่ง Django ทั้งหมด

ใน repository นี้ไม่มี `requirements.txt` และไม่ได้ pin เวอร์ชัน Django ไว้ ถ้าเครื่องที่ใช้ยังไม่มี Django ให้ติดตั้ง Django ใน Python ที่ใช้งานก่อน โดยโปรเจกต์นี้ไม่ต้องตั้งค่า database server เพิ่มเพราะใช้ SQLite ที่มากับ Django

ถ้าเริ่มจากโฟลเดอร์ว่าง คำสั่งสร้าง project และ app มีรูปแบบดังนี้ (ใน repository นี้สร้างไว้แล้ว จึงไม่ต้องรันซ้ำ):

```bash
django-admin startproject core .
python3 manage.py startapp todo
```

จากนั้นเพิ่ม `'todo'` ใน `INSTALLED_APPS` ของ `core/settings.py` กำหนด route กลางใน `core/urls.py` และ route ของ Todo ใน `todo/urls.py` Django แยก project กับ app เพื่อให้ project หนึ่งรวม app ได้หลายชุด

**ไฟล์ที่เกี่ยวข้อง:** `manage.py`, `core/settings.py`

---

## บทที่ 1: ทำความเข้าใจการเดินทางของ request

เมื่อเปิดหน้า Todo list ลำดับการทำงานเป็นดังนี้:

```text
Browser → core/urls.py → todo/urls.py → todo/views.py → todo/models.py → template → HTML response
```

ตัวอย่าง เมื่อเปิด `/todos/5/edit/`:

1. Django อ่าน URL แล้วเข้า `core/urls.py`
2. `include('todo.urls')` ส่งต่อการค้นหา route ไปที่ `todo/urls.py`
3. Django ส่งเลข `5` ให้ view ชื่อ `todo_edit` เป็นค่า `pk`
4. View หา Todo หมายเลข 5 จากฐานข้อมูล
5. View สร้าง `TodoForm` โดยใส่ Todo เดิมเป็น `instance`
6. Django render `todo/templates/todo/edit.html`
7. Browser แสดงแบบฟอร์มแก้ไข

เมื่อผู้ใช้กด Save browser ส่ง POST request กลับ URL เดิม View ตรวจ form ก่อนบันทึก

**ลองทำ:** เปิด `core/urls.py` แล้วดูว่า URL หลักส่งต่อไปที่ไฟล์ใด จากนั้นเปิด `todo/urls.py` เพื่อหา route ของหน้า list, create และ edit และดูชื่อ view ที่แต่ละ route เรียก

**แบบฝึกหัด:** วาดแผนภาพการกดปุ่ม Complete โดยเริ่มจากปุ่มใน list template จนสถานะใน SQLite เปลี่ยน

---

## บทที่ 2: URL และการเชื่อมหน้าเข้ากับ View

การตั้งค่า URL มีสองระดับเพื่อแยก route ของเว็บไซต์ออกจาก route ของ Todo app ไฟล์ `core/urls.py` ดูแล route ระดับ project และส่ง route ของ Todo ต่อให้ app:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('todo.urls')),
    path('admin/', admin.site.urls),
]
```

`include('todo.urls')` บอก Django ให้ค้นหา route ต่อในไฟล์ของ app โดยไม่เพิ่ม URL prefix เพราะ prefix เป็นสตริงว่าง `''`; `/admin/` ยังคงจัดการที่ระดับ project

เนื้อหาทั้งหมดของ `todo/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('todos/create/', views.todo_create, name='todo_create'),
    path('todos/<int:pk>/edit/', views.todo_edit, name='todo_edit'),
    path('todos/<int:pk>/delete/', views.todo_confirm_delete, name='todo_confirm_delete'),
    path('todos/<int:pk>/complete/', views.todo_complete, name='todo_complete'),
    path('todos/<int:pk>/cancel/', views.todo_cancel, name='todo_cancel'),
]
```

`path('todos/<int:pk>/edit/', ...)` แปลว่า URL ต้องมีเลขจำนวนเต็มตรงตำแหน่ง `pk` เช่น `/todos/5/edit/` ชื่อที่กำหนดด้วย `name='todo_edit'` ช่วยให้ template อ้าง URL ได้โดยไม่ hardcode:

```django
<a href="{% url 'todo_edit' todo.pk %}">Edit</a>
```

หากเปลี่ยน path ใน Python ชื่อ route ยังคงเดิม template จะสร้าง URL ใหม่ได้เอง

### แบบฝึกหัด

1. เพิ่ม route `/about/` ที่แสดงหน้าแนะนำแอป
2. ตั้งชื่อ route ว่า `about` แล้วเรียก route จาก template ด้วย `{% url 'about' %}`
3. อธิบายว่าเหตุใด route ที่มี `<int:pk>` จึงต้องระบุ `pk` ตอนสร้าง URL

**ไฟล์อ้างอิง:** `core/urls.py`, `todo/urls.py`

---

## บทที่ 3: Model, field และฐานข้อมูล

เปิด `todo/models.py` Model `Todo` กำหนดคอลัมน์ของรายการงาน:

```python
from django.db import models


class Todo(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'todo'
        verbose_name_plural = 'todos'

    def __str__(self):
        return self.title
```

อธิบายทีละส่วน:

- `models.Model` ทำให้ Django รู้ว่า class นี้เป็น model และเชื่อมกับตารางฐานข้อมูล
- `CharField` เก็บข้อความสั้น ต้องกำหนดความยาวสูงสุดด้วย `max_length`
- `TextField` เก็บรายละเอียดข้อความ และ `blank=True` ทำให้เว้นว่างจากฟอร์มได้
- `TextChoices` ประกาศค่าสถานะที่อนุญาตไว้จุดเดียว ลดความผิดพลาดจากการพิมพ์ข้อความเอง
- `default=Status.PENDING` ตั้งสถานะเริ่มต้นเมื่อสร้างรายการ
- `auto_now_add=True` ตั้งวันเวลาเพียงตอนสร้าง record; `editable=False` ทำให้ field นี้ไม่ปรากฏใน ModelForm
- `Meta.ordering` ให้รายการใหม่อยู่บนสุด
- `__str__` กำหนดข้อความแทน object ใน admin และ shell

### สร้าง migration

หลังเพิ่มหรือเปลี่ยน field ห้ามแก้ `db.sqlite3` ด้วยมือ ให้ Django สร้าง migration:

```bash
python3 manage.py makemigrations todo
python3 manage.py migrate
```

`makemigrations` เปรียบเทียบ model กับ migration เดิมและสร้างไฟล์ใน `todo/migrations/` ไฟล์ `0001_initial.py` ในโปรเจกต์นี้สร้างตาราง `Todo` ครั้งแรก `migrate` นำการเปลี่ยนแปลงไปใช้กับ SQLite

ตรวจดูการเปลี่ยนแปลงก่อน apply ได้ด้วย:

```bash
python3 manage.py sqlmigrate todo 0001
```

### ทดลอง ORM ผ่าน shell

```bash
python3 manage.py shell
```

จากนั้นพิมพ์ Python:

```python
from todo.models import Todo

task = Todo.objects.create(
    title='Learn Django ORM',
    description='Create my first model record',
)
task.status
Todo.objects.all()
Todo.objects.filter(status=Todo.Status.PENDING)
Todo.objects.order_by('-created_at')
```

ORM คือ API ของ Django สำหรับอ่านและแก้ข้อมูลโดยใช้ Python แทนการต่อ SQL ด้วย string

### แบบฝึกหัด

เพิ่ม `priority` ด้วยตัวเลือก `low`, `normal`, `high` และค่าเริ่มต้น `normal` จากนั้นสร้าง migration แล้วใช้ shell สร้าง task ระดับ high

**ไฟล์อ้างอิง:** `todo/models.py`, `todo/migrations/0001_initial.py`, `core/settings.py`

---

## บทที่ 4: Form และ validation

ไฟล์ `todo/forms.py` ใช้ ModelForm เพื่อสร้างช่องกรอกและตรวจชนิดข้อมูลจาก model:

```python
from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a task title',
                'autofocus': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add details about this task',
                'rows': 3,
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'status': 'Status',
        }
```

`fields` เป็น allowlist: ระบุ field ที่ผู้ใช้แก้ได้ชัดเจน ในตัวอย่างไม่มี `created_at` จึงไม่รับวันสร้างจาก request ส่วน `widgets` ปรับชนิด HTML และ class ให้เข้ากับ Bootstrap

การตรวจข้อมูลเกิดก่อนบันทึก:

```python
form = TodoForm(request.POST)
if form.is_valid():
    todo = form.save()
```

ถ้าข้อมูลไม่ผ่าน validation ให้ render form กลับไปพร้อม `form.errors` อย่าบันทึกค่าจาก `request.POST` ลง database โดยตรง

**แบบฝึกหัด:** เปลี่ยน label หรือ placeholder ใน `forms.py` แล้วตรวจว่าข้อความเปลี่ยนในหน้า Create และ Edit โดยไม่แก้ HTML ซ้ำ

**ไฟล์อ้างอิง:** `todo/forms.py`, `todo/templates/todo/create.html`, `todo/templates/todo/edit.html`

---

## บทที่ 5: View และ CRUD

View ปัจจุบันอยู่ใน `todo/views.py` ด้านล่างเป็นไฟล์เต็ม โดยแต่ละ function รับ request และส่ง response กลับ Django:

```python
from datetime import date

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .forms import TodoForm
from .models import Todo


@require_GET
def todo_list(request):
    query = request.GET.get('q', '').strip()
    created_date = request.GET.get('created_date', '').strip()
    todos = Todo.objects.all()

    if query:
        todos = todos.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if created_date:
        try:
            parsed_date = date.fromisoformat(created_date)
        except ValueError:
            todos = todos.none()
        else:
            todos = todos.filter(created_at__date=parsed_date)

    return render(request, 'todo/todo_list.html', {
        'todos': todos,
        'query': query,
        'created_date': created_date,
    })


@require_http_methods(['GET', 'POST'])
def todo_create(request):
    form = TodoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Task created successfully.')
        return redirect('todo_list')
    return render(request, 'todo/create.html', {
        'form': form,
        'today': timezone.localdate(),
        'submit_label': 'Create Task',
    })


@require_http_methods(['GET', 'POST'])
def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    form = TodoForm(request.POST or None, instance=todo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Task updated successfully.')
        return redirect('todo_list')
    return render(request, 'todo/edit.html', {
        'form': form,
        'todo': todo,
        'submit_label': 'Save Changes',
    })


@require_http_methods(['GET', 'POST'])
def todo_confirm_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('todo_list')
    return render(request, 'todo/confirm_delete.html', {'todo': todo})


@require_POST
def todo_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.status = Todo.Status.COMPLETED
    todo.save(update_fields=['status'])
    messages.success(request, 'Task marked as complete.')
    return redirect('todo_list')


@require_POST
def todo_cancel(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.status = Todo.Status.CANCELLED
    todo.save(update_fields=['status'])
    messages.success(request, 'Task cancelled.')
    return redirect('todo_list')
```

ตัวแปรที่พบบ่อยใน view:

- `request` คือข้อมูล request จาก browser เช่น path, method และค่าฟอร์ม
- `request.GET` คือข้อมูล query string เช่น `/?q=meeting`
- `request.POST` คือข้อมูลที่ browser ส่งมาพร้อม POST form
- `render(request, template, context)` ประกอบ template กับข้อมูลแล้วส่ง HTML response
- `redirect('todo_list')` ตอบกลับให้ browser ไปยัง URL ที่ผูกกับชื่อ route นั้น
- `context` เป็น dictionary ที่ส่ง Python data เข้า template เช่น `{'todos': todos}` ทำให้ template ใช้ `{{ todos }}` ได้

### อ่าน view ทีละกลุ่ม

**Read:** `todo_list` รับ GET, สร้าง queryset และส่งให้ template ผ่าน dictionary `context` การค้นหาคำใช้ `Q(...) | Q(...)` ซึ่งเทียบเท่าเงื่อนไข OR

**Create:** GET แสดง form ว่าง ส่วน POST bind ข้อมูลจาก browser, เรียก `is_valid()`, บันทึกด้วย `save()` แล้ว redirect กลับ list

**Update:** `TodoForm(..., instance=todo)` บอก Django ว่าให้แก้ record เดิม หากไม่มี `instance` Django จะสร้าง record ใหม่แทน

**Delete:** GET แสดงหน้ายืนยัน ส่วน POST เรียก `delete()` วิธีนี้ป้องกันการลบจากการเปิดลิงก์ด้วย GET

**Complete/Cancel:** เป็น action ที่เปลี่ยนเฉพาะ status จึงจำกัด method ด้วย `@require_POST` และบันทึกเฉพาะ field ที่เปลี่ยนด้วย `update_fields`

**404:** `get_object_or_404` ช่วยจัดการกรณี ID ไม่มีอยู่โดยไม่ต้องเขียน try/except เอง

**Messages:** `messages.success` ฝากข้อความไว้แสดงหลัง redirect ระบบ messages เปิดใช้งานผ่าน middleware และ context processor ใน `core/settings.py`

### แบบฝึกหัด

1. เพิ่ม route และ view สำหรับเปลี่ยน task กลับเป็น Pending
2. เพิ่ม filter สถานะโดยรับ `status` จาก GET และตรวจว่าใช้พร้อมกับ `q` ได้
3. เปลี่ยนข้อความ success ให้แจ้งชื่อ task ที่เพิ่งแก้

---

## บทที่ 6: HTML templates และ template inheritance

### 6.1 Layout กลาง

`todo/templates/base.html` เก็บโครง HTML ที่แชร์ร่วมกัน ทุก page template ใช้ `{% extends 'base.html' %}` ทำให้ sidebar, Bootstrap, CSS และ messages ไม่ต้องเขียนซ้ำ:

```html
{% load static %}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Todo List{% endblock %} | Taskflow</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
  <link href="{% static 'todo/css/main.css' %}" rel="stylesheet">
  {% block extra_head %}{% endblock %}
</head>
<body>
  <div class="app-shell">
    <aside class="sidebar">
      <a class="brand" href="{% url 'todo_list' %}" aria-label="Taskflow home">
        <span class="brand-icon">✓</span><span>Taskflow</span>
      </a>
      <div class="sidebar-label">WORKSPACE</div>
      <a class="sidebar-link {% if request.resolver_match.url_name == 'todo_list' %}active{% endif %}" href="{% url 'todo_list' %}">
        <span class="nav-icon">▤</span><span>Todo List</span>
      </a>
      <div class="sidebar-footer">
        <span class="avatar">T</span>
        <div><strong>My Workspace</strong><small>Personal tasks</small></div>
      </div>
    </aside>

    <main class="main-area">
      <div class="content-wrap">
        {% if messages %}
          {% for message in messages %}
            <div class="alert alert-success alert-dismissible fade show" role="status">
              {{ message }}
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
          {% endfor %}
        {% endif %}
        {% block content %}{% endblock %}
      </div>
    </main>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
  {% block extra_js %}{% endblock %}
</body>
</html>
```

`{% load static %}` เปิดใช้ tag สำหรับ static files; `{% block content %}` คือพื้นที่ที่ child template เติมเนื้อหา

### 6.2 หน้า list

`todo/templates/todo/todo_list.html` แสดง search form และวนรายการจาก context ชื่อ `todos`:

```html
{% extends 'base.html' %}

{% block title %}Your Tasks{% endblock %}

{% block content %}
<section class="panel list-panel">
  <div class="list-heading">
    <div class="list-title-group">
      <span class="section-kicker">YOUR TASKS</span>
      <h1>Todo List <span class="count-pill">{{ todos|length }}</span></h1>
    </div>
    <form class="search-form" method="get" action="{% url 'todo_list' %}">
      <div class="search-input-wrap">
        <span class="search-symbol" aria-hidden="true">⌕</span>
        <input class="form-control" type="search" name="q" value="{{ query }}" placeholder="Search title or description" aria-label="Search title or description">
      </div>
      <input class="form-control date-filter" type="date" name="created_date" value="{{ created_date }}" aria-label="Filter by creation date">
      <button class="btn btn-outline-primary" type="submit">Search</button>
      {% if query or created_date %}<a class="clear-link" href="{% url 'todo_list' %}">Clear</a>{% endif %}
    </form>
    <a class="btn btn-primary new-task-button" href="{% url 'todo_create' %}"><span class="plus">＋</span> New Task</a>
  </div>

  {% if todos %}
    <div class="table-responsive">
      <table class="table todo-table align-middle mb-0">
        <thead><tr><th>Task</th><th>Status</th><th>Created</th><th class="text-end">Actions</th></tr></thead>
        <tbody>
          {% for todo in todos %}
            <tr>
              <td class="task-cell">
                <div class="task-title">{{ todo.title }}</div>
                {% if todo.description %}<div class="task-description">{{ todo.description|linebreaksbr }}</div>{% else %}<div class="task-description muted">No description</div>{% endif %}
              </td>
              <td>
                {% if todo.status == 'completed' %}<span class="status-badge status-completed"><i></i>Completed</span>
                {% elif todo.status == 'cancelled' %}<span class="status-badge status-cancelled"><i></i>Cancelled</span>
                {% else %}<span class="status-badge status-pending"><i></i>Pending</span>{% endif %}
              </td>
              <td class="date-cell">{{ todo.created_at|date:"j M Y" }}<small>{{ todo.created_at|date:"H:i" }}</small></td>
              <td>
                <div class="action-group">
                  <a class="action-button action-edit" href="{% url 'todo_edit' todo.pk %}" aria-label="Edit {{ todo.title }}">Edit</a>
                  <form method="post" action="{% url 'todo_complete' todo.pk %}">
                    {% csrf_token %}<button class="action-button action-complete" type="submit">Complete</button>
                  </form>
                  <form method="post" action="{% url 'todo_cancel' todo.pk %}">
                    {% csrf_token %}<button class="action-button action-cancel" type="submit">Cancel</button>
                  </form>
                  <a class="action-button action-delete" href="{% url 'todo_confirm_delete' todo.pk %}">Delete</a>
                </div>
              </td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  {% else %}
    <div class="empty-state">
      <div class="empty-icon">✓</div>
      {% if query or created_date %}<h2>No matching tasks</h2><p>Try another search term or creation date.</p>
      {% else %}<h2>No tasks yet</h2><p>Create your first task to get started.</p>{% endif %}
    </div>
  {% endif %}
</section>
{% endblock %}
```

ค่าที่ render ด้วย `{{ ... }}` จะถูก HTML-escape โดย Django เป็นค่าเริ่มต้น หลีกเลี่ยง `safe` กับข้อมูลที่ผู้ใช้กรอกเอง ใช้ GET ใน search เพราะ URL ที่ได้บอกเงื่อนไขค้นหาและ refresh ได้

### 6.3 หน้า Create และ Edit

ทุกหน้าเป็น template แยกและ extends `base.html` ตัวอย่างไฟล์ `todo/templates/todo/create.html`:

```html
{% extends 'base.html' %}

{% block title %}Create Task{% endblock %}

{% block content %}
<section class="panel form-panel">
  <div class="section-heading">
    <div><span class="section-kicker">NEW TASK</span><h1>Create Task</h1></div>
  </div>
  <form method="post" novalidate>
    {% csrf_token %}
    <div class="form-grid">
      <div class="field-group field-title">
        <label for="{{ form.title.id_for_label }}">Title <span class="required-mark">*</span></label>
        {{ form.title }}
        {% for error in form.title.errors %}<div class="field-error">{{ error }}</div>{% endfor %}
      </div>
      <div class="field-group field-status">
        <label for="{{ form.status.id_for_label }}">Status</label>
        {{ form.status }}
        {% for error in form.status.errors %}<div class="field-error">{{ error }}</div>{% endfor %}
      </div>
      <div class="field-group field-description">
        <label for="{{ form.description.id_for_label }}">Description</label>
        {{ form.description }}
        {% for error in form.description.errors %}<div class="field-error">{{ error }}</div>{% endfor %}
      </div>
      <div class="field-group field-created">
        <label for="created_at_display">Created Date</label>
        <input id="created_at_display" class="form-control readonly-date" type="date" value="{{ today|date:'Y-m-d' }}" readonly aria-describedby="created-help">
        <small id="created-help">Set automatically and cannot be changed.</small>
      </div>
    </div>
    <div class="form-actions">
      <a class="btn btn-light px-4" href="{% url 'todo_list' %}">Back to Tasks</a>
      <button class="btn btn-primary px-4" type="submit">Create Task</button>
    </div>
  </form>
</section>
{% endblock %}
```

`todo/templates/todo/edit.html` ใช้ markup ลักษณะเดียวกัน แต่เปลี่ยนหัวข้อและวันที่เป็น `{{ todo.created_at|date:'Y-m-d' }}` ปุ่ม submit เป็น Save Changes ตัวอย่างฟอร์มที่ edit ใช้เหมือน create ยกเว้น context `todo` ที่ส่งจาก view

วันที่ที่เห็นใน input เป็นเพียงการแสดงผลแบบ readonly เท่านั้น Django กำหนดค่า `created_at` จริงจาก model ไม่เชื่อค่าจาก browser

ตัวอย่างไฟล์เต็มสำหรับแก้ไข `todo/templates/todo/edit.html`:

```html
{% extends 'base.html' %}

{% block title %}Edit Task{% endblock %}

{% block content %}
<section class="panel form-panel">
  <div class="section-heading">
    <div><span class="section-kicker">UPDATE TASK</span><h1>Edit Task</h1></div>
  </div>
  <form method="post" novalidate>
    {% csrf_token %}
    <div class="form-grid">
      <div class="field-group field-title">
        <label for="{{ form.title.id_for_label }}">Title <span class="required-mark">*</span></label>
        {{ form.title }}
        {% for error in form.title.errors %}<div class="field-error">{{ error }}</div>{% endfor %}
      </div>
      <div class="field-group field-status">
        <label for="{{ form.status.id_for_label }}">Status</label>
        {{ form.status }}
        {% for error in form.status.errors %}<div class="field-error">{{ error }}</div>{% endfor %}
      </div>
      <div class="field-group field-description">
        <label for="{{ form.description.id_for_label }}">Description</label>
        {{ form.description }}
        {% for error in form.description.errors %}<div class="field-error">{{ error }}</div>{% endfor %}
      </div>
      <div class="field-group field-created">
        <label for="created_at_display">Created Date</label>
        <input id="created_at_display" class="form-control readonly-date" type="date" value="{{ todo.created_at|date:'Y-m-d' }}" readonly aria-describedby="created-help">
        <small id="created-help">Set automatically and cannot be changed.</small>
      </div>
    </div>
    <div class="form-actions">
      <a class="btn btn-light px-4" href="{% url 'todo_list' %}">Back to Tasks</a>
      <button class="btn btn-primary px-4" type="submit">Save Changes</button>
    </div>
  </form>
</section>
{% endblock %}
```

ความต่างสำคัญคือ view ส่ง `todo` มาด้วยเพื่อแสดงวันที่เดิม และส่ง `TodoForm(..., instance=todo)` เพื่ออัปเดต record เดิม

### 6.4 หน้ายืนยันลบ

ไฟล์ `todo/templates/todo/confirm_delete.html` ต้องแสดงการยืนยันแยกก่อนส่ง POST:

```html
{% extends 'base.html' %}

{% block title %}Confirm Delete{% endblock %}

{% block content %}
<section class="panel confirm-panel">
  <div class="section-heading">
    <div><span class="section-kicker">DELETE TASK</span><h1>Confirm Delete</h1></div>
  </div>
  <div class="delete-warning-icon">!</div>
  <h2>Delete “{{ todo.title }}”?</h2>
  <p class="confirm-copy">This action cannot be undone. The task and its details will be permanently removed.</p>
  {% if todo.description %}<div class="confirm-description">{{ todo.description|linebreaksbr }}</div>{% endif %}
  <form method="post" class="form-actions confirm-actions">
    {% csrf_token %}
    <a class="btn btn-light px-4" href="{% url 'todo_list' %}">Cancel</a>
    <button class="btn btn-danger px-4" type="submit">Delete Task</button>
  </form>
</section>
{% endblock %}
```

ทุก form ที่เปลี่ยนข้อมูลใช้ POST และ `{% csrf_token %}` ส่วนหน้า list เองก็ extends `base.html` แม้จะมี form สำหรับ search และปุ่ม Complete/Cancel อยู่ภายใน

**ไฟล์อ้างอิง:** `todo/templates/base.html`, `todo/templates/todo/todo_list.html`, `create.html`, `edit.html`, `confirm_delete.html`

---

## บทที่ 7: CSS, Bootstrap และ Responsive UI

Bootstrap ช่วยเรื่อง grid, form controls, buttons และ table ส่วน CSS ของโปรเจกต์อยู่ใน `todo/static/todo/css/main.css` ใช้ `{% static 'todo/css/main.css' %}` โหลดจาก `base.html`

ตัวอย่าง stylesheet แบบเต็มสำหรับเริ่มฝึก ให้บันทึกใน `todo/static/todo/css/lesson.css` และเพิ่ม link ใน `base.html` ถ้าต้องการทดลองแยกจาก style จริง:

```css
:root {
  --blue: #316fea;
  --navy: #152b4a;
  --muted: #77849a;
  --line: #e8edf4;
  --page: #f5f7fb;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  color: #1e293b;
  background: var(--page);
  font-family: Arial, sans-serif;
}
.app-shell { min-height: 100vh; }
.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  width: 230px;
  padding: 24px 18px;
  background: white;
  border-right: 1px solid var(--line);
}
.brand { color: var(--navy); font-size: 20px; font-weight: 700; text-decoration: none; }
.sidebar-link { display: block; margin-top: 36px; padding: 12px; color: var(--blue); text-decoration: none; }
.main-area { margin-left: 230px; padding: 36px; }
.content-wrap { max-width: 1180px; margin: 0 auto; }
.panel { overflow: hidden; background: white; border: 1px solid var(--line); border-radius: 14px; }
.list-heading { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 22px; }
.section-kicker { color: #94a3b8; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
.list-heading h1 { color: var(--navy); font-size: 20px; }
.search-form { display: flex; flex-wrap: wrap; gap: 8px; }
.form-control { min-height: 38px; padding: 8px 10px; border: 1px solid #dce3ed; border-radius: 8px; }
.btn { display: inline-block; padding: 10px 14px; border: 1px solid var(--blue); border-radius: 8px; text-decoration: none; cursor: pointer; }
.btn-primary { color: white; background: var(--blue); }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 14px 18px; border-top: 1px solid var(--line); text-align: left; }
.table th { color: var(--muted); background: #fafbfd; font-size: 12px; }
.task-description, .empty-state p { color: var(--muted); font-size: 13px; }
.empty-state { padding: 48px 20px; text-align: center; }
.form-panel, .confirm-panel { max-width: 760px; margin: 0 auto; padding: 24px; }
.form-panel label { display: block; margin: 14px 0 6px; font-weight: 600; }
.form-panel textarea { min-height: 90px; }
.field-error { color: #c03945; font-size: 13px; }

@media (max-width: 760px) {
  .sidebar { position: static; width: 100%; padding: 16px; border-right: 0; border-bottom: 1px solid var(--line); }
  .sidebar-link { display: inline-block; margin: 8px 0 0; }
  .main-area { margin-left: 0; padding: 18px 12px; }
  .list-heading { align-items: flex-start; flex-direction: column; }
  .search-form, .search-form input { width: 100%; }
  .table th, .table td { padding: 10px 8px; }
}
```

CSS selector เช่น `.sidebar` เลือก element ที่มี class ชื่อนั้น; `@media` เปลี่ยน layout เมื่อจอกว้างไม่เกิน 760px; CSS variables ที่ `:root` ช่วยให้เปลี่ยนสีหลักจากจุดเดียว

**แบบฝึกหัด:** เปลี่ยนสี primary, ลดความกว้าง sidebar และตรวจหน้าใน browser ทั้ง desktop และหน้าจอแคบ

---

## บทที่ 8: Django Admin และ settings

`todo/admin.py` ทำให้ Todo ใช้ผ่าน admin ได้:

```python
from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')
```

เปิด `/admin/` และลงชื่อเข้าใช้ด้วย superuser หากยังไม่มีบัญชี สร้างด้วย `python3 manage.py createsuperuser` Admin เหมาะสำหรับผู้ดูแลและงานตรวจข้อมูล ไม่ได้แทนหน้า UI สำหรับผู้ใช้ทั่วไป

ไฟล์ `todo/admin.py` ฉบับเต็มในโปรเจกต์มีเพียงการ register และตั้งค่าคอลัมน์/ตัวกรอง:

```python
from django.contrib import admin

from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')
```

ค่าที่ควรรู้ใน `core/settings.py`:

- `INSTALLED_APPS`: เปิดใช้งาน `todo` และ Django built-in apps
- `MIDDLEWARE`: มี security, session, CSRF, authentication และ messages middleware
- `TEMPLATES['APP_DIRS']`: ให้ Django ค้นหา templates ภายใน app
- `DATABASES`: ใช้ SQLite ที่ `BASE_DIR / 'db.sqlite3'`
- `LANGUAGE_CODE = 'en-us'`, `TIME_ZONE = 'UTC'`, `USE_TZ = True`
- `STATIC_URL`: URL prefix สำหรับ static files

ในการ deploy จริง ต้องใช้ secret key ที่เป็นความลับ, ปิด `DEBUG`, และตั้ง `ALLOWED_HOSTS` ตามโดเมนจริง ค่า settings ปัจจุบันเป็นค่าพัฒนาท้องถิ่น Todo routes ยังไม่ได้บังคับ login แม้ authentication middleware จะเปิดอยู่—middleware เพียงแนบข้อมูลผู้ใช้กับ request ไม่ได้บังคับ login โดยอัตโนมัติ

---

## บทที่ 9: เขียน Test เบื้องต้น

ใน repository ปัจจุบัน `todo/tests.py` ยังเป็น placeholder การเขียน test ช่วยตรวจพฤติกรรมซ้ำได้เมื่อแก้โค้ดภายหลัง เพิ่มตัวอย่างนี้ใน `todo/tests.py`:

```python
from django.test import TestCase
from todo.models import Todo


class TodoModelTests(TestCase):
    def test_new_task_defaults_to_pending_and_gets_created_date(self):
        task = Todo.objects.create(title='Practice testing')

        self.assertEqual(task.status, Todo.Status.PENDING)
        self.assertIsNotNone(task.created_at)
```

รัน test ด้วย:

```bash
python3 manage.py test
```

แบบฝึกหัดเพิ่ม: ใช้ Django test client เรียกหน้า `/`, POST ไปหน้า create, ตรวจว่ารายการถูกสร้าง และตรวจว่าการเรียก Complete ด้วย GET ไม่สำเร็จเพราะ view อนุญาตเฉพาะ POST

---

## บทที่ 10: โปรเจกต์ฝึกระดับกลาง — Personal Task Board

ต่อยอด Todo app ให้รองรับการวางแผนงานรายสัปดาห์ โดยทำทีละขั้น:

1. เพิ่ม `priority` และ `due_date` ใน `todo/models.py`
2. สร้าง migration และ migrate
3. เพิ่ม fields ใน `todo/forms.py` โดยกำหนด widget และ label
4. แสดง fields ใน `create.html` และ `edit.html`; ห้ามให้ผู้ใช้แก้ `created_at`
5. เพิ่มตัวกรอง priority/due date ใน `todo/views.py` และ controls ใน `todo_list.html`
6. แสดง overdue tasks ด้วย class ใน `todo/static/todo/css/main.css`
7. เพิ่ม priority และ due date ใน admin list/search/filter ตามความเหมาะสม
8. เพิ่ม tests สำหรับ default priority, date filter, overdue state และ status actions

### เกณฑ์ว่าสำเร็จ

- ผู้ใช้สร้าง อ่าน แก้ไข และลบรายการได้
- Complete/Cancel เปลี่ยน status ผ่าน POST และมี CSRF token
- Search title/description และ filters ใช้ร่วมกันได้
- `created_at` เกิดจาก server และแก้จาก form ไม่ได้
- URL ที่อ้าง record ที่ไม่มีอยู่ตอบ 404
- หน้าไม่มีผลลัพธ์แสดง empty state และหน้าจอเล็กยังใช้งานได้
- Migration และ tests ผ่าน

---

## ทบทวนความรู้และลำดับแนะนำ

1. ทำบทที่ 0–2 แล้วอธิบายได้ว่า URL ส่ง request ไปถึง view อย่างไร
2. ทำบทที่ 3 และทดลองเพิ่ม/ค้นข้อมูลด้วย ORM
3. ทำบทที่ 4–6 โดยติดตามข้อมูลจาก form ผ่าน view ไปยัง model และกลับมาแสดงใน template
4. ทำบทที่ 7–9 เพื่อปรับ UI, จัดการ admin, security และ test
5. ทำ Personal Task Board โดยเพิ่มทีละ field และทดสอบทุกขั้น

เมื่อเจอปัญหา ให้ตรวจตามลำดับนี้: URL ถูกต้องหรือไม่ → view รับ method ถูกหรือไม่ → form valid หรือไม่ → migration ถูก apply หรือยัง → context key ตรงกับ template หรือไม่ → browser console/terminal มี error อะไร
