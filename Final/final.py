
import os
import sys
import time
import shutil
import random
import string
import multiprocessing
from APIFramework import APIFramework, APIFrameworkWithFrontEnd, queue


import vis_driver


class Final(APIFrameworkWithFrontEnd):

    def form_task(self, p):
        res = {}

        # task_str = p["original_file_name"].encode("utf-8")
        list_id = self.str2hash( ''.join(random.choice(string.ascii_lowercase) for i in range(100)).encode("utf-8") )

        res["id"] = list_id

        return res


    def worker(self, pid, task_queue, result_queue, suicide_queue_pair, params):

        self.output(2, "Worker-%s is starting up" % (pid))

        self.output(2, "Worker-%s is ready to take job" % (pid))

        while True:
            task_detail = self.task_queue_get(task_queue, pid, suicide_queue_pair)

            self.output(2, "Worker-%s is computing task: %s" % (pid, task_detail))

            error = []
            calculation_start_time = time.time()

            try:
                os.mkdir("./task/")
            except:
                pass

            list_id = task_detail["id"]
            result = []

            working_dir = "./task/" + list_id + "/"
            input_file = working_dir + "/data.txt"
            os.mkdir(working_dir)
            shutil.copy("./input/%s" % list_id, input_file)

            # result = vis.your_function(working_dir)
            # result = list(map(lambda x: working_dir+x, result))

            result_tmp = vis_driver.generate_all_vis(working_dir)


            result = []
            for triple in result_tmp:
                # image relative path, type, column name
                result.append(triple[0])


            calculation_end_time = time.time()
            calculation_time_cost = calculation_end_time - calculation_start_time

            self.output(2, "Worker-%s finished computing job (%s)" % (pid, list_id))

            res = {
                "id": list_id,
                "start time": calculation_start_time,
                "end time": calculation_end_time,
                "runtime": calculation_time_cost,
                "error": error,
                "result": result
            }

            self.output(2, "Job (%s): %s" % (list_id, res))

            result_queue.put(res)




if __name__ == '__main__':
    multiprocessing.freeze_support()

    glylookup_app = Final()
    glylookup_app.find_config("final.ini")
    glylookup_app.start()










