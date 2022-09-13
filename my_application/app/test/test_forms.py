import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from app.forms import ReportForm


class TestForms(SimpleTestCase):
    def test_report_form_valid(self):
        form = ReportForm(data={})
        assert form.is_valid() is False

        file_path = os.path.join('app\\test\\test_files', 'file_1_ok.csv')

        with open(file_path, 'rb') as f:
            form = ReportForm(data={'name': "my_report"}, files={'data': SimpleUploadedFile('file_1_ok.csv', f.read())})
        assert form.is_valid(), 'Invalid form, errors: {}'.format(form.errors)

    def test_report_form_invalid_not_csv(self):
        file_path = os.path.join('app\\test\\test_files', 'file_6_fail')

        with open(file_path, 'rb') as f:
            form = ReportForm(data={'name': "my_report"},
                              files={'data': SimpleUploadedFile('file_6_fail', f.read())})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_report_form_invalid_column_name(self):
        file_path = os.path.join('app\\test\\test_files', 'file_2_fail.csv')

        with open(file_path, 'rb') as f:
            form = ReportForm(data={'name': "my_report"},
                              files={'data': SimpleUploadedFile('file_2_fail.csv', f.read())})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_report_form_invalid_empty_amount(self):
        file_path = os.path.join('app\\test\\test_files', 'file_3_fail.csv')

        with open(file_path, 'rb') as f:
            form = ReportForm(data={'name': "my_report"},
                              files={'data': SimpleUploadedFile('file_3_fail.csv', f.read())})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_report_form_invalid_country_alpha2(self):
        file_path = os.path.join('app\\test\\test_files', 'file_4_fail.csv')

        with open(file_path, 'rb') as f:
            form = ReportForm(data={'name': "my_report"},
                              files={'data': SimpleUploadedFile('file_4_fail.csv', f.read())})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_report_form_invalid_string_amount(self):
        file_path = os.path.join('app\\test\\test_files', 'file_5_fail.csv')

        with open(file_path, 'rb') as f:
            form = ReportForm(data={'name': "my_report"},
                              files={'data': SimpleUploadedFile('file_5_fail.csv', f.read())})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
