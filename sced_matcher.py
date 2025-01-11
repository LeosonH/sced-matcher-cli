from openai import OpenAI
import time

with open('gpt_apikey.txt') as api_key:
    openai_key = api_key.readline()


def main():
    user_input = input("Enter Course Name or Description: ")
    
    client = OpenAI(api_key=openai_key)

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input.strip().replace('/', '')
    )

    my_updated_assistant = client.beta.assistants.update(
      "asst_PbpkEKciHCmAJS4Yf4uKAUV5",
        tool_resources={
        "code_interpreter": {
          "file_ids": ["file-kino7A5APplnta6Alp1x8xx7"]
        }
      }, model="gpt-4o"
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id='asst_PbpkEKciHCmAJS4Yf4uKAUV5',
        #instructions="Be sure to search your .csv file thoroughly. Output the closest matching SCED code based on course name and course description. If there are numerous matches, choose the one most similar to the user input. Format your response with only the SCED Code, Course Title, and Course Description you found in the knowledge base, each separated by an comma, and do not include anything else."
    )

    # Waits for the run to be completed. 
    while True:
        print(".")
        print(".")
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, 
                                                       run_id=run.id)
        if run_status.status == "completed":
            print(".")
            print("Done!")
            print("")
            break
        elif run_status.status == "failed":
            print("Run failed:", run_status.last_error)
            break
        time.sleep(2)  # wait for 2 seconds before checking again
        
    messages = client.beta.threads.messages.list(thread_id=thread.id)
                
    answer = messages.data[0].content[0].text.value.split(",")

    if int(answer[0]) < 10000:
        sced_code = '0' + str(answer[0])
    else:
        sced_code = answer[0]
    print("SCED_code: " + sced_code)
    print("")

    course_name = answer[1]
    print("Course Name: " + course_name)
    print("")

    course_description = answer[2]
    print("Course Description: " + course_description)
    
if __name__ == '__main__':
    main()