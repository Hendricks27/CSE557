
import os
import sys
import time
import shutil
import random
import string
import multiprocessing
from APIFramework import APIFramework, APIFrameworkWithFrontEnd, queue

import evaluation
import vis_driver


class Final(APIFrameworkWithFrontEnd):

    def form_task(self, p):
        res = {}

        # task_str = p["original_file_name"].encode("utf-8")
        list_id = self.str2hash( ''.join(random.choice(string.ascii_lowercase) for i in range(100)).encode("utf-8") )

        res["id"] = list_id
        res["task_type"] = p["task_type"]

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
            task_type = task_detail["task_type"]

            working_dir = "./task/" + list_id + "/"
            input_file = working_dir + "/data.txt"
            os.mkdir(working_dir)
            shutil.copy("./input/%s" % list_id, input_file)

            result_tmp = vis_driver.generate_all_vis(working_dir)

            """
            tmpd = {0: 'Correlation', 1: 'Anomalies', 2: 'Clusters', 3: 'Distribution', 4: 'Range'}
            tmpdr = {}
            for k,v in tmpd.items():
                tmpdr[v] = k
            """
            vis_selection_tmp = evaluation.main(input_file, task_type)

            vis_selection = {}
            for v in vis_selection_tmp:
                graph_type = v.pop(0)
                columns = tuple(sorted(v))
                vis_selection[columns] = graph_type


            # Single Column Graph: table, aligned bar, box plot, density plot, ???
            # 2      Column Graph: scatter plot, ???

            result = []
            for triple in result_tmp:
                # image relative path, type, column name
                columns_name = tuple(sorted(triple[2]))

                print(triple[1], vis_selection.get(columns_name, None))

                if vis_selection.get(columns_name, None) == triple[1]:
                    result.append(triple[0])
                else:
                    pass
                    #print(columns_name, triple[1], "discarded")


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










