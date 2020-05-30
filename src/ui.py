from PyInquirer import prompt
from .utils import Action, FollowUpAction, is_file, SpinnerThread
from typing import List, Dict
from progress.spinner import Spinner
from time import sleep
import tkinter as tk
from tkinter import filedialog


class UI():

    @staticmethod
    def display_message(message: str):
        print(message)

    @staticmethod
    def prompt_action():
        questions: List[Dict[str, Any]] = [
            {
                'type': 'list',
                'name': 'action',
                'message': 'What action do yo want to perform',
                'click': False,
                'choices': [
                    {
                        'name': Action.SEND.value,
                    },
                    {
                        'name': Action.RECEIVE.value
                    }
                ]
            }
        ]
        return prompt(questions)['action']

    @staticmethod
    def prompt_follow_up_action():
        questions: List[Dict[str, Any]] = [
            {
                'type': 'list',
                'name': 'follow_up_action',
                'message': 'Send another file or go home',
                'click': False,
                'choices': [
                    {
                        'name': FollowUpAction.SEND_ANOTHER.value,
                    },
                    {
                        'name': FollowUpAction.RETURN_HOME.value,
                    }
                ]
            }
        ]
        return prompt(questions)['follow_up_action']

    @staticmethod
    def prompt_hosts(hosts):
        questions: List[Dict[str, Any]] = [
            {
                'type': 'list',
                'name': 'host',
                'message': 'Which device do you want to connect to',
                'click': False,
                'choices': [{'name': f"{name} {ip}"} for ip, name in hosts]

            }
        ]
        return prompt(questions)['host'].split(' ')[-1]

    @staticmethod
    def get_file():
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(title='Select a file to send')
        filepath = '' if filepath is None else filepath
        while not is_file(filepath):
            filepath = filedialog.askopenfilename(
                title='Select a file to send')
        return filepath

    @staticmethod
    def get_spinner(message: str):
        spinner_thread = SpinnerThread(Spinner(message+' '))
        spinner_thread.start()
        return spinner_thread

    @staticmethod
    def stop_spinner(spinner: SpinnerThread):
        spinner.stop()
        sleep(.1)
        print('\n')
