<em> Note from timm: these files were too large for git checkin. for full download, please see https://struebli.informatik.uni-freiburg.de/downloads/re2019-artifact.zip</em>
## README
This file contains descriptions and installation instructions for the artifact of the RE 2019 paper *Scalable Analysis of Real-Time Requirements*.

**Note:** If you do not have a markdown renderer on hand you can refer to the file ``README.html`` which is a plain HTML rendering of this file. 

### What does the artifact do?
This artifact allows you to re-run the experiments detailed in Section  *VII. EVALUATION AND APPLICATION* of our paper. 
It will produce a log file that contains the columns from Table 1 and Table 2.
It contains all the requirement files and the binaries of all the tools used in our experiments. 

### Contents of the archive
You have received the artifact in form of a ``.zip`` file which contains the following things.
  * ``benchexec/`` contains [benchexec](https://github.com/sosy-lab/benchexec) 1.18-dev, which we use to execute the experiments in parallel and take exact measures of time and memory consumption.
  * ``req2ta/`` contains req2ta, a part of the tool used in [17] to implement their method. 
  * ``uppaal64-4.1.22/`` contains [UPPAAL](http://www.uppaal.org) 4.1.22, a model checking tool for timed automata.
  * ``req2ta2UPPAAL.sh``, a shell script that combines req2ta and UPPAAL to check requirements for rt-inconsistency (i.e., the tool described in [17]).
  * ``UAutomizer-linux/`` contains Ultimate ReqAnalyzer 0.1.24-4f1d294 (i.e., our implementation of the method described in our paper), which is based on the [Ultimate program analysis framework](https://github.com/ultimate-pa/ultimate). **Note that this is a newer version than the one in the paper**.
  * ``run-experiments.sh``, a shell script that runs all the experiments described in Section VII of the paper (i.e., produces the results from Table 1 and Table 2) using benchexec, then extracts the results from the logs of Ultimate ReqAnalyzer and req2ta2UPPAAL and pretty-prints them.
  * ``reqs/`` contains the anonymised formalized requirements used in Table 1 and Table 2. The naming scheme of the ``.req`` file is ``part<X>_<id>.<old|new>?.req``. ``X`` specifies where in the Table you have to look. Table 1 is split in four parts from top to bottom (as described in the paper), Table 2 is the fifth part. ``<id>`` is the identifier found in the respective *ID* columns of Table 1 and 2. Because the syntax of the ``.req`` files is slightly different between the two tools, all files for Table 1 come in two variants. ``old`` is the syntax of req2ta2UPPAAL, ``new`` the syntax of Ultimate ReqAnalyzer. 
  * Various descriptive files that are used to define the benchmarks
    * ``benchexec_def_req2ta2UPPAAL_part1_to_3.xml``, ``part1-old.set``, ``part2-old.set``, and ``part3-old.set`` define the benchmark run that produces the result from Table 1 for the column req2ta2UPPAAL except the ``all`` file, 
    * ``benchexec_def_req2ta2UPPAAL_part4.xml`` and ``part4-old.set`` define the benchmark run that produces the result from Table 1 for the column req2ta2UPPAAL and only the ``all`` file, 
    * ``benchexec_def_ultimate_reqanalyzer_part1_to_3.xml``, ``part1-new.set``, ``part2-new.set``, and ``part3-new.set`` define the benchmark run that produces the result from Table 1 for the column Ultimate ReqAnalyzer except ``all`` file, 
    * ``benchexec_def_ultimate_reqanalyzer_part4.xml`` and ``part4-new.set`` define the benchmark run that produces the result from Table 1 for the column Ultimate ReqAnalyzer and only the ``all`` file, 
    * ``benchexec_def_ultimate_reqanalyzer_part5.xml`` defines the benchmark run that produces the result from Table 2, and
    * ``non-deadlock.q`` is a query file that is used as input to UPPAAL to specify that UPPAAL should search for deadlocks, and
  * ``README.md`` this file.
  * ``README.html`` a HTML version of this file.
  * ``INSTALL.md`` a near-empty file. Installation instructions can be found in this file. 
  * ``LICENSE.md`` a file describing all the licenses the different tools in this artifact use. Short summary: all are LGPLv3 compatible.
  * ``STATUS.md`` explains for which badge we apply and why.
  * ``req2ta-tmp-output/`` is an empty folder where req2ta will put the generated timed automata before ``req2ta2UPPAAL.sh`` passes them on to UPPAAL.
  * ``eval-results-original.log`` is the log file obtained by running ``run-experiments.sh`` with all benchmarks enabled.

## Installation instructions 


### System requirements
In order to run the artifact you will need a 64-bit Linux system with the following features.
  * bash >= 4.2 (should be available on all modern Linux systems)
  * Java JDK 8
  * python3
  * the python packages tempita and yaml (easily obtainable with ``pip3 install --user pyyaml tempita``
  * enabled cgroups support (cgroups is a Linux kernel feature necessary for benchexec -- [they have an good documentation on how-to enable cgroups](https://github.com/sosy-lab/benchexec/blob/master/doc/INSTALL.md#setting-up-cgroups))

If your system does not already satisfies these requirements or if you do not want to install / configure it such that it does, you can [download a virtual machine from us](https://struebli.informatik.uni-freiburg.de/tap2019ae/tap2019.ova) that has all the necessary tools available. It is roughly 3GB in size. 
We used [VirtualBox 6.0](https://www.virtualbox.org) to create this virtual machine. 
The username is ``tap2019`` with password ``tap2019``. The root user has the same password. 

**Note** You need 32GB of usable system memory to run all the experiments. 8GB is enough if you only want to run the experiments from Table 1 without part 4 (the ``all`` file). 

### Running the experiments
In order to run the experiments, first open the file ``run-experiments.sh`` in your favorite editor. 
In the beginning you see an array named benchmarks:
````
benchmarks=(
  req2ta2UPPAAL_part1_to_3
  ultimate_reqanalyzer_part1_to_3
#  req2ta2UPPAAL_part4
#  ultimate_reqanalyzer_part4
#  ultimate_reqanalyzer_part5
)
````
These five strings control which benchmarks to run. Comment or uncomment them as you see fit. 
The script will try and determine the maximum number of benchmarks it can run in parallel on your machine.
On our machine (32 cores with 128GB of memory) the runtimes were approximately as follows for both tools together.
  * ``*part1_to_3`` specifies parts 1 to 3 of Table 1 and should run fairly fast (approx. 30min)
  * ``*part4`` has a timeout of 9000s and will take that time for req2ta2UPPAAL
  * ``*part5`` is the complete Table 2 and will take approx. 12h

The script will create a log file ``eval-results.log`` where it will place the results and the data of the experiments (specified by ``log_file="eval-results.log"``). 
At the beginning of its execution, it will delete all temporary files from the last run. These are the following.
  * ``req2ta-tmp-output/`` is an empty folder where req2ta will put the generated timed automata before ``req2ta2UPPAAL.sh`` passes them on to UPPAAL.
  * ``results/`` is the directory where benchexec will store the raw log files and the output of req2ta2UPPAAL,
  * ``UAutomizer-linux/results`` is the directory where benchexec will store the raw log files and the output of Ultimate ReqAnalyzer, 
  * ``eval-results.log`` is the last log file

If you are satisfied with your configuration, you can go ahead and run the script directly from this folder by typing``./run-experiments.sh``.

## FAQ
### Is the artifact installed and working correctly?
First check that only the benchmarks ``req2ta2UPPAAL_part1_to_3`` and ``ultimate_reqanalyzer_part1_to_3`` are enabled at the beginning of the file ``run-experiments.sh``. It should look like this:
````
benchmarks=(
  req2ta2UPPAAL_part1_to_3
  ultimate_reqanalyzer_part1_to_3
#  req2ta2UPPAAL_part4
#  ultimate_reqanalyzer_part4
#  ultimate_reqanalyzer_part5
)
````
If you now execute ``./run-experiments.sh``, you should see output similar to the following:
````
# ./run-experiments.sh
####### Running benchmark req2ta2UPPAAL_part1_to_3 ######
Using 15 threads
2019-06-30 08:32:18,318 - WARNING - No propertyfile specified. Score computation will ignore the results.

executing run set 'req2ta2UPPAAL'     (29 files)
08:32:18   starting   part1_02.old.req
08:32:18   starting   part1_03.old.req
08:32:18   starting   part1_04.old.req
08:32:18   starting   part1_05.old.req
08:32:18   starting   part1_06.old.req
08:32:18   starting   part2_03.old.req
08:32:18   starting   part2_06.old.req
08:32:18   starting   part2_07.old.req
08:32:18   starting   part2_08.old.req
08:32:18   starting   part2_09.old.req
08:32:18   starting   part2_10-prime.old.req
08:32:18   starting   part2_10.old.req
08:32:18   starting   part3_01.old.req
08:32:18   starting   part3_02.old.req
08:32:18   starting   part3_03.old.req
08:32:19              part2_10.old.req          unknown                   0.86    0.54
08:32:19   starting   part3_04.old.req
08:32:19              part3_01.old.req          unknown                   0.74    0.53
08:32:19   starting   part3_05.old.req
08:32:19              part2_08.old.req          unknown                   0.92    0.60
08:32:19   starting   part3_06.old.req
08:32:19              part1_04.old.req          unknown                   1.04    0.70
08:32:19   starting   part3_07.old.req
08:32:19              part1_05.old.req          unknown                   1.21    0.76
08:32:19   starting   part3_08.old.req
08:32:19              part2_09.old.req          unknown                   1.56    0.87
08:32:19   starting   part3_09.old.req
08:32:19              part3_07.old.req          unknown                   0.39    0.28
08:32:19   starting   part3_10.old.req
08:32:19              part3_06.old.req          unknown                   0.76    0.49
08:32:19   starting   part3_11.old.req
08:32:19              part3_08.old.req          unknown                   0.85    0.51
08:32:19   starting   part3_12.old.req
08:32:19              part3_04.old.req          unknown                   1.07    0.66
08:32:19   starting   part3_13.old.req
08:32:20              part3_03.old.req          unknown                   2.17    1.43
08:32:20   starting   part3_14.old.req
08:32:20              part3_11.old.req          unknown                   0.38    0.29
08:32:20   starting   part3_15.old.req
08:32:20              part3_12.old.req          unknown                   0.33    0.26
08:32:20   starting   part3_16.old.req
08:32:20              part3_13.old.req          unknown                   0.36    0.27
08:32:20   starting   part3_17.old.req
08:32:20              part3_17.old.req          unknown                   0.31    0.24
08:32:20              part3_15.old.req          unknown                   0.55    0.36
08:32:21              part2_10-prime.old.req    unknown                   3.46    2.44
08:32:32              part1_03.old.req          unknown                  21.41   13.75
08:32:36              part2_06.old.req          unknown                  25.03   18.04
08:33:45              part1_06.old.req          unknown                  93.67   86.68
08:33:57              part2_07.old.req          unknown                 110.29   98.53
08:34:33              part1_02.old.req          unknown                 142.14  135.04
08:36:00              part3_16.old.req          unknown                 227.47  220.12
08:37:57              part3_02.old.req          unknown                 379.67  339.00
08:38:24              part3_05.old.req          unknown                 413.27  365.14
08:44:45              part3_09.old.req          unknown                 752.36  745.76
08:45:05              part3_10.old.req          TIMEOUT                 900.38  765.05
08:45:06              part2_03.old.req          OUT OF MEMORY           781.96  767.43
08:46:46              part3_14.old.req          TIMEOUT                 900.55  865.42

Statistics:             29 Files
  correct:               0
    correct true:        0
    correct false:       0
  incorrect:             0
    incorrect true:      0
    incorrect false:     0
  unknown:              29

In order to get HTML and CSV tables, run
benchexec/bin/table-generator 'results/benchexec_def_req2ta2UPPAAL_part1_to_3.2019-06-30_0832.results.req2ta2UPPAAL.xml'
INFO:     results/benchexec_def_req2ta2UPPAAL_part1_to_3.2019-06-30_0832.results.req2ta2UPPAAL.xml
INFO: Merging results...
INFO: Generating table...
INFO: Missing property for reqs/part1_02.old.req.
INFO: Missing property for reqs/part1_03.old.req.
INFO: Missing property for reqs/part1_04.old.req.
INFO: Missing property for reqs/part1_05.old.req.
INFO: Missing property for reqs/part1_06.old.req.
INFO: Missing property for reqs/part2_03.old.req.
INFO: Missing property for reqs/part2_06.old.req.
INFO: Missing property for reqs/part2_07.old.req.
INFO: Missing property for reqs/part2_08.old.req.
INFO: Missing property for reqs/part2_09.old.req.
INFO: Missing property for reqs/part2_10-prime.old.req.
INFO: Missing property for reqs/part2_10.old.req.
INFO: Missing property for reqs/part3_01.old.req.
INFO: Missing property for reqs/part3_02.old.req.
INFO: Missing property for reqs/part3_03.old.req.
INFO: Missing property for reqs/part3_04.old.req.
INFO: Missing property for reqs/part3_05.old.req.
INFO: Missing property for reqs/part3_06.old.req.
INFO: Missing property for reqs/part3_07.old.req.
INFO: Missing property for reqs/part3_08.old.req.
INFO: Missing property for reqs/part3_09.old.req.
INFO: Missing property for reqs/part3_10.old.req.
INFO: Missing property for reqs/part3_11.old.req.
INFO: Missing property for reqs/part3_12.old.req.
INFO: Missing property for reqs/part3_13.old.req.
INFO: Missing property for reqs/part3_14.old.req.
INFO: Missing property for reqs/part3_15.old.req.
INFO: Missing property for reqs/part3_16.old.req.
INFO: Missing property for reqs/part3_17.old.req.
INFO: Writing HTML into results/benchexec_def_req2ta2UPPAAL_part1_to_3.2019-06-30_0832.results.req2ta2UPPAAL.html ...
INFO: Writing CSV  into results/benchexec_def_req2ta2UPPAAL_part1_to_3.2019-06-30_0832.results.req2ta2UPPAAL.csv ...
INFO: done
### req2ta2UPPAAL ###
ID       rt-inc.         Time
part1_02.old.req        rt-inconsistent  142.135982395
part1_03.old.req        rt-inconsistent  21.409659899
part1_04.old.req        rt-consistent    1.041136068
part1_05.old.req        rt-consistent    1.207790384
part1_06.old.req        rt-inconsistent  93.667632149
part2_03.old.req         OUT OF MEMORY   781.963725882
part2_06.old.req        rt-inconsistent  25.026852181
part2_07.old.req        rt-consistent    110.293581288
part2_08.old.req        rt-consistent    0.919939447
part2_09.old.req        rt-consistent    1.557850091
part2_10.old.req        rt-consistent    0.864513377
part2_10-prime.old.req  rt-consistent    3.456706013
part3_01.old.req        rt-consistent    0.73602275
part3_02.old.req        rt-consistent    379.670228739
part3_03.old.req        rt-consistent    2.17308414
part3_04.old.req        rt-consistent    1.07298554
part3_05.old.req        rt-consistent    413.274359635
part3_06.old.req        rt-inconsistent  0.760368067
part3_07.old.req        rt-consistent    0.38955836
part3_08.old.req        rt-consistent    0.849840077
part3_09.old.req        rt-consistent    752.357041967
part3_10.old.req         TIMEOUT         900.375576034
part3_11.old.req        rt-consistent    0.381226939
part3_12.old.req        rt-consistent    0.328692008
part3_13.old.req        rt-inconsistent  0.358935419
part3_14.old.req         TIMEOUT         900.546394439
part3_15.old.req        rt-consistent    0.548473462
part3_16.old.req        rt-consistent    227.469453005
part3_17.old.req        rt-inconsistent  0.312133277

####### Running benchmark ultimate_reqanalyzer_part1_to_3 ######
...

````
You can see the following things.
  * The script determines the number of threads for your system. You might have less or more threads, i.e., the line ``Using 15 threads`` might show a different number. 
  * The script starts benchexec for the given benchmark with the determined number of threads. The last line of benchexec's output is ``In order to get HTML and CSV tables, run...``
  * Then, the script runs the table-generator to generate a ``.csv`` file from the benchexec results. The last line here is ``INFO: done``.
  * Afterwards, the script parses the output of the respective tool (in our example req2ta2UPPAAL) and the ``.csv`` file to generate a small table that corresponds to a part of either Table 1 or Table 2 (in the example, Table 1 part 1 to 4) and prints that to the console. It also writes this table to the file ``eval-results.log``.

### I get error messages, what do they mean?
**Q:** I see the following message
``WARNING - CPU throttled itself during benchmarking due to overheating. Benchmark results are unreliable!``, what does it mean. 
**A:** You are probably running the experiment on a notebook and the cooling system is insufficient to keep the CPU at a stable frequency. This leads to longer runtimes. You should be ok if this message occurs for all of the benchmarks. If not, the benchmarks with this warning took longer then one could assume given your hardware. 

**Q:**  ``CRITICAL - Kernel misses feature for accounting swap memory, but machine has swap. Please set swapaccount=1 on your kernel command line or disable swap with "sudo swapoff -a"``
**A:**  benchexec wants to measure the consumed memory, and it cannot do that reliably if it cannot measure the swap memory consumption. You can easily disable swap before running the benchmarks and reenable it afterwards: 
````
sudo swapoff -a
./run-experiments.sh
sudo swapon -a
````

**Q:** I see the following messages:
````
WARNING - Cannot determine Ultimate version (API 2). Exit code : 13 Command was java -Xss4m -jar ./plugins/org.eclipse.equinox.launcher_1.3.100.v20150511-1540.jar -data @noDefault -ultimatedata ./data --version
WARNING - Cannot determine Ultimate version (API 1). Exit code : 13 Command was java -Xss4m -jar ./plugins/org.eclipse.equinox.launcher_1.3.100.v20150511-1540.jar -data ./data --version
Error: Could not determine Ultimate version
````
**A:** You do not have the correct Java version installed. Check that ``java -version`` says that you have ``java version "1.8.0_xxx"``


### Which results can be expected to differ from the results shown in the paper?
Since the submission, we updated our tool Ultimate ReqAnalyzer.
  * We fixed a bug that prevented us from finding all rt-inconsistencies in a given requirement set. The fix might lead to slow-downs depending on the requirement set.
  * We improved the performance in some cases. 

Hence, some examples have different rt-inconsistency numbers compared to the paper, and some are significantly faster or slower. 

Because we expect most reviewers do not have enough memory in their system, we reduced the memory limit for Table 2 to 32GB and the number of cores to 4 (instead of 100GB and 32 cores). Furthermore, we set a timeout of 1 day instead of no timeout at all. 

In particular, the following results are different.
#### Table 1 Ultimate ReqAnalyzer
| ID | Vac. | rt-inc. | T. |
|--|--|--|--|
| part2_09 | 0 | 0 | 32.07 instead of 93.86 |
| part3_09 | 0 | 0 | 39.92 instead of 318.65 |
| part3_10 | 1 | 89 instead of 60 | 283.30 instead of 816.70 |
| part3_14 | 0 | 0 | 21.59 instead of 87.62 |

#### Table 2
| ID               |  Vac.         |  rt-inc.      |  TO           |  Time              |
|--|--|--|--|--|
| part5_dev01.req  | 0 | 6 instead of 0  | 0 | 261.30 instead of 5 |
| part5_dev02.req  | 0 | 13 instead of 8 | 0 instead of 3 | 3757.53 instead of 1882|
| part5_dev03.req  | 0 | 0               | 0 instead of 1| 115.90 instead of 380|
| part5_dev04.req  | 0 | 13 instead of 8 | 0 instead of 3| 5596.28 instead of 1343|
| part5_dev05.req  | 0 | 4               | 1 instead of 2| 5902.93 instead of 683|
| part5_dev06.req  | 0 (TIMEOUT)  | 3 (TIMEOUT) instead of 5  |  7 (TIMEOUT) instead of 1 | 21600.45+ instead of 506 |
| part5_dev07.req  | 0 | 38            | 0 instead of 2 | 18514.28 instead of 923|
| part5_dev08.req  |  6 (TIMEOUT)  |  53 (TIMEOUT) instead of 73 |  48 (TIMEOUT) instead of 18 | 21600.32+ instead of 14316 |
| part5_dev09.req  |  2 (TIMEOUT)  |  39 (TIMEOUT) instead of 33 |  79 (TIMEOUT) instead of 0 | 21600.78+ instead of 11586|
| part5_dev10.req  |  1 (TIMEOUT)  |  0 (TIMEOUT)  |  47 (TIMEOUT) instead of 11 | 21600.20+ instead of 17093|

The file ``eval-results-original.log`` contains the results we obtained with the current version and the current setup. We will update the paper for the camera-ready to reflect these changes. 
Although Table 2 shows significantly longer runtimes, we also find more errors. The slow-down is also not unreasonable large; we can still produce useful results within a day. 
We also believe that we can recover much of the speed we lost to the bug fix in yet another update of our tool. Unfortunately, we do not have enough time to add this update before the deadline. 
