#include <process.h>
#include <cstring>
#include <cstdio>
// usage: (calling by CMCL main process)
// Restarter [executable_pid_name] [python_env]
int main(const int argc,char **argv){
    if (argc==1){
        return -1;
    }else{
        char* exe_pid_name = argv[1];
        char executable[100]{};
        if (argc>2){
            strcpy(executable,argv[2]);
        }
        char* task_kill_command = new char[150];
        sprintf(task_kill_command,"taskkill /f /im %s",exe_pid_name);
        system(task_kill_command);
        
        if (strlen(executable)>0){
            system(executable);
        }
        return 0;
    }
}