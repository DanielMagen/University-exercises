#include "sleeping_threads_list.h"

SleepingThreadsList::SleepingThreadsList() {
}


/*
 * Description: This method adds a new element to the list of sleeping
 * threads. It gets the thread's id, and the time when it needs to wake up.
 * The wakeup_tv is a struct timeval (as specified in <sys/time.h>) which
 * contains the number of seconds and microseconds since the Epoch.
 * The method keeps the list sorted by the threads' wake up time.
*/
void SleepingThreadsList::add(int thread_id, timeval wakeup_tv) {

    wake_up_info new_thread;
    new_thread.id = thread_id;
    new_thread.awaken_tv = wakeup_tv;

    if (sleeping_threads.empty()) {
        sleeping_threads.push_front(new_thread);
    } else {
        for (deque<wake_up_info>::iterator it = sleeping_threads.begin();
             it != sleeping_threads.end(); ++it) {
            if (timercmp(&it->awaken_tv, &wakeup_tv, >=)){
                sleeping_threads.insert(it, new_thread);
                return;
            }
        }
        sleeping_threads.push_back(new_thread);
    }
}

/*
 * Description: This method removes the thread at the top of this list.
 * If the list is empty, it does nothing.
*/
void SleepingThreadsList::pop() {
    if (!sleeping_threads.empty())
        sleeping_threads.pop_front();
}

void SleepingThreadsList::deleteFromList(int id) {
    for (auto it = sleeping_threads.begin(); it != sleeping_threads.end(); ++it) {
        if (it->id == id) {
            sleeping_threads.erase(it);
            return;
        }
    }
}

/*
 * Description: This method returns the information about the thread (id and time it needs to wake up)
 * at the top of this list without removing it from the list.
 * If the list is empty, it returns null.
*/
wake_up_info *SleepingThreadsList::peek() {
    if (sleeping_threads.empty())
        return nullptr;
    return &sleeping_threads.at(0);
}

time_t SleepingThreadsList::getSecondsSinceEpochOfHead() {
    timeval awaken_tv = peek()->awaken_tv;
    return awaken_tv.tv_sec * 1000000 + awaken_tv.tv_usec;
}

