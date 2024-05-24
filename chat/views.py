from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import redirect
from chat.models import Chat, Requests, Messages
from user.models import get_user_by_id, get_company_by_user_id
from fastnumbers import isfloat
from .utils import chat_gpt

def chat(request, chat_id):
    user_id = request.session.get('user_id')
    user = get_user_by_id(user_id)[0]
    chats = Chat.objects.filter(id = chat_id, owner = user_id)
    data = {}
    if len(chats):
        chat = chats.last()
        messages = Messages.objects.filter(chat = chat_id).order_by('-index').values()
        data['messages'] = messages.values()
        data['chat'] = chat

        if request.method == 'POST':

            content = str(request.POST['message_content'])
            
            gpt_messages = [
                {"role": "system", "content": f"{chat.system_prompt}"}
            ]
            for m in messages[::-1]:
                gpt_messages.append(
                    {"role": f"{m['role']}", "content": f"{m['content']}"}
                )

            gpt_messages.append(
                {"role": 'user', "content": f"{content}"}
            )
            response = chat_gpt(gpt_messages, int(chat.max_tokens), float(chat.presence_penalty), float(chat.top_p))

            request_info = {}
            request_info['chat'] = chat
            request_info['response'] = response
            request_info['owner_id'] = user_id
            try:
                output_tokens = int(response.usage.completion_tokens)
                input_tokens = int(response.usage.prompt_tokens)
                request_info['output_tokens'] = output_tokens
                request_info['input_tokens'] = input_tokens
                request_info['cost'] = (0.50 * (input_tokens/1e6)) + (1.50 * (output_tokens/1e6))
            except Exception as e:
                request_object = Requests(**request_info)
                request_object.save()
                print(e)
                data['error'] = str(e)
                return render(request, 'chat.html', data)

            request_object = Requests(**request_info)
            request_object.save()

            try:
                response_text = response.choices[0].message.content
            except Exception as e:
                print(e)
                data['error'] = str(e)
                return render(request, 'chat.html', data)

            input_message = {}
            input_message['chat'] = chat
            input_message['content'] = content
            latest = Messages.objects.filter(chat = chat_id, owner = user_id).order_by('-index').first()
            
            if latest:
                input_message['index'] = int(latest.index) + 1
            else:
                input_message['index'] = 1
            input_message['owner_id'] = user_id
            input_message['role'] = 'user'
            input_message['tokens'] = len(content)//4
            
            input_object = Messages(**input_message)
            input_object.save()

            output_message = {}
            output_message['chat'] = chat
            output_message['content'] = response_text
            output_message['index'] = input_message['index'] + 1
            output_message['owner_id'] = user_id
            output_message['role'] = 'assistant'
            output_message['tokens'] = output_tokens

            output_object = Messages(**output_message)
            output_object.save()
            
            return render(request, 'chat.html', data)

        return render(request, 'chat.html', data)
    
    return render(request, '404.html')

def chats_panel(request):
    data = {}
    data['chats'] = Chat.objects.all().order_by('-date_created').values()

    for i, chat in enumerate(data['chats']):
        cost = sum([m.cost if isfloat(m.cost) else 0 for m in Requests.objects.filter(chat = chat['id'])])
        data['chats'][i]['total_cost'] = cost

    return render(request, 'chats_panel.html', data)

def add(request):
    user_id = request.session.get('user_id')
    
    data = {}
    insert_fields = {}
    if request.method == 'POST':
        print(request.POST)

        if 'chatname' not in request.POST:
            data['error'] = 'Please enter a name.'
        
        elif request.POST['chatname'] == '':
            data['error'] = 'Please enter a name.'

        elif not isfloat(str(request.POST['presence_penalty'])):
            data['error'] = 'Invalid value for presence penalty.'

        elif not isfloat(str(request.POST['top_p'])):
            data['error'] = 'Invalid value for top p.'

        elif not isfloat(str(request.POST['max_tokens'])):
            data['error'] = 'Invalid value for max tokens.'

        else:
            insert_fields['name'] = request.POST['chatname']
            insert_fields['owner_id'] = user_id
            insert_fields['presence_penalty'] = round(float(request.POST['presence_penalty']), 1)
            insert_fields['top_p'] = round(float(request.POST['top_p']), 1)
            insert_fields['max_tokens'] = int(request.POST['max_tokens'])
            insert_fields['is_active'] = (request.POST['is_active'] == 'Active')
            
            if 'description' not in request.POST:
                insert_fields['description'] = ''
            else:
                insert_fields['description'] = request.POST['description']

            if 'system_prompt' not in request.POST:
                insert_fields['system_prompt'] = ''
            else:
                insert_fields['system_prompt'] = request.POST['system_prompt']
                

            p = Chat(**insert_fields)
            p.save()

            return redirect('/mychats/view/' + str(p.pk))

    return render(request, 'create_chat.html', data)

def edit(request, chat_id):
    user_id = request.session.get('user_id')
    chats = Chat.objects.filter(id = chat_id, owner = user_id)
    data = {}
    if len(chats):

        update_field = {}
        if request.method == 'POST':
            print(request.POST)

            if 'chatname' in request.POST:
                if request.POST['chatname'] != '':
                    update_field['name'] = request.POST['chatname']

            if isfloat(str(request.POST['presence_penalty'])):
                update_field['presence_penalty'] = round(float(request.POST['presence_penalty']), 1)

            if isfloat(str(request.POST['top_p'])):
                update_field['top_p'] = round(float(request.POST['top_p']), 1)

            if isfloat(str(request.POST['max_tokens'])):
                update_field['max_tokens'] = int(request.POST['max_tokens'])

            update_field['owner_id'] = user_id
            update_field['is_active'] = (request.POST['is_active'] == 'Active')
            
            if 'description' in request.POST:
                update_field['description'] = request.POST['description']

            if 'system_prompt' in request.POST:
                update_field['system_prompt'] = request.POST['system_prompt']

            chats.update(**update_field)
            chat = chats.last()
            data['chat'] = chat
            
            data['success'] = "Data saved successfully."
            return render(request, 'edit_chat.html', data)

        chat = chats.last()
        data['chat'] = chat
        return render(request, 'edit_chat.html', data)
    
    return render(request, '404.html')

def detail(request):
    return render(request, 'chat_detail.html')

def delete(request, chat_id):

    insert_fields = {}
    data = {}
    if request.method == 'POST':
        Chat.objects.filter(id=chat_id).delete()
        return redirect('/mychats/')