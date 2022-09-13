from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import render, redirect
import pandas as pd
from app import Analysis
from app.forms import ReportForm
from app.models import Report


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
@transaction.atomic
def show_profile(request):

    my_reports = list(reversed((Report.objects.filter(Creator=request.user))))
    return render(request, 'profile.html', {'my_reports': my_reports})


def show_report(request, id):

    report = Report.objects.get(id=id)

    return render(request, 'Report.html', {'report': report})


def create_report(request):
    form = ReportForm

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            my_report = form.save(commit=False)
            my_report.Creator = request.user
            my_report.save()
            analyse_response = Analysis.analyse(my_report.data.file)

            saved_report = Report.objects.get(id=my_report.id)

            output_file_path = "media/files/output/" + request.user.username + "_" + saved_report.name + "_" +\
                               str(saved_report.id) + "_output.xlsx"

            with pd.ExcelWriter(output_file_path) as writer:
                analyse_response[4].to_excel(writer, sheet_name='initial_transactions')
                analyse_response[1].to_excel(writer, sheet_name='local_transactions')
                analyse_response[0].to_excel(writer, sheet_name='cycles_flows')
                analyse_response[5].to_excel(writer, sheet_name='local_countries')

            saved_report.output_data.name = "files/output/" + request.user.username + "_" + saved_report.name + "_" \
                                            + str(saved_report.id) + "_output.xlsx"

            saved_report.total_local_transactions = analyse_response[2]
            saved_report.total_initial_transactions = analyse_response[3]
            saved_report.no_of_initial_transactions = analyse_response[6]
            saved_report.no_of_initial_countries = analyse_response[7]
            saved_report.no_of_local_countries = analyse_response[8]
            saved_report.no_of_cycles_flows = analyse_response[9]
            saved_report.no_of_local_transactions = analyse_response[10]
            saved_report.no_complete_local_transactions = analyse_response[11]

            saved_report.save()

            return redirect('show_profile')

    return render(request, 'Report_form.html', {'form': form})


