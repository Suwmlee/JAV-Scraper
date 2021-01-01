# -*- coding: utf-8 -*-
''' task
'''
from ..model.task import _Task
from .. import db


class TaskService():

    def getTask(self, taskname):
        task = _Task.query.filter_by(name=taskname).first()
        if not task:
            task = _Task(taskname)
            db.session.add(task)
            db.session.commit()
        return task

    def updateTaskStatus(self, status, taskname):
        """ status
            0: wait
            1: finished
            2: runing
        """
        task = self.getTask(taskname)
        if task.status != status:
            task.status = status
            db.session.commit()

taskService = TaskService()
