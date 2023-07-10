from django.shortcuts import render, redirect
from . forms import ProjectForm, ReviewForm
from .models import Project, Review, Tag
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def projects(request):
    projects = Project.objects.all()
    context ={
        'projects': projects
    }
    print(projects)
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        print("reviewrs", project.reviewers)
        project.getVoteCount
        messages.success(request, "Review was submitted successfully")
        return redirect('project', pk=project.id)
        
        
        # Update Project Vote Count
        
        
    context ={
        'project': project,
        'form': form
    }
    return render(request, 'projects/single-project.html', context)


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == 'POST':
        
        newtags = request.POST.get('newtags').replace(",", " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    
    context ={
        'form': form
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(",", " ").split()
        print("data:", newtags)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    else:
        form = ProjectForm(instance=project)
        context ={
            'form': form,
            'project': project
        }
    return render(request, 'projects/project_form.html', context)




@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context ={
            'object': project
        }
    return render(request, 'delete_template.html', context)
    

