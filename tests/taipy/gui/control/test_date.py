from datetime import datetime

from taipy.gui import Gui


def test_date_md_1(gui: Gui, helpers):
    gui.bind_var_val("date", datetime.strptime("15 Dec 2020", "%d %b %Y"))
    md_string = "<|{date}|date|>"
    expected_list = ["<DateSelector", 'defaultDate="2020-12-', 'tp_varname="TaipyDate_date"', "date={TaipyDate_date}"]
    helpers.test_control_md(gui, md_string, expected_list)


def test_date_md_2(gui: Gui, helpers):
    gui.bind_var_val("date", datetime.strptime("15 Dec 2020", "%d %b %Y"))
    md_string = "<|{date}|date|with_time|>"
    expected_list = ["<DateSelector", 'defaultDate="2020-12-',
                     'tp_varname="TaipyDate_date"', "date={TaipyDate_date}", "withTime={true}"]
    helpers.test_control_md(gui, md_string, expected_list)


def test_date_html_1(gui: Gui, helpers):
    gui.bind_var_val("date", datetime.strptime("15 Dec 2020", "%d %b %Y"))
    html_string = '<taipy:date date="{date}" />'
    expected_list = ["<DateSelector", 'defaultDate="2020-12-', 'tp_varname="TaipyDate_date"', "date={TaipyDate_date}"]
    helpers.test_control_html(gui, html_string, expected_list)


def test_date_html_2(gui: Gui, helpers):
    gui.bind_var_val("date", datetime.strptime("15 Dec 2020", "%d %b %Y"))
    html_string = "<taipy:date>{date}</taipy:date>"
    expected_list = ["<DateSelector", 'defaultDate="2020-12-', 'tp_varname="TaipyDate_date"', "date={TaipyDate_date}"]
    helpers.test_control_html(gui, html_string, expected_list)