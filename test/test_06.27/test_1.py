import openai

# API�L�[��ݒ肵�Ă��������B��: 'your-api-key'
#api_key = 'uBulLxdhNUxkWjw7x3veT3BlbkFJGBD21ioNk3j5wNEnDFV6'
#openai.api_key = api_key

openai.api_key = ""

def generate_text(prompt, role, conversation_history):
    # ���[�U�[�̎������b�����ɒǉ�
    conversation_history.append({"role": "user", "content": prompt})
    
    # GPT-4���f�����g�p���ăe�L�X�g�𐶐�
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": f"You are a {role}."}] + conversation_history,
        max_tokens=50,
        n=1,
        temperature=0.8,
    )
    message = response.choices[0].message['content'].strip()
    
    # �A�V�X�^���g�̉񓚂���b�����ɒǉ�
    conversation_history.append({"role": "assistant", "content": message})
    
    return message

if __name__ == "__main__":
    # ���[���v���C�̃��f�������[�U�[�ɓ��͂�����
    role = input("���[���v���C�̃��f�����w�肵�Ă��������i��: helpful assistant�j: ")
    
    # ��b�������i�[���邽�߂̃��X�g��������
    conversation_history = []
    
    while True:
        # ���[�U�[�Ɏ������͂�����
        input_prompt = input("�������͂��Ă��������i�I������ɂ�'q'����́j: ")
        
        # �I�������̊m�F
        if input_prompt.lower() == 'q':
            break
        
        # GPT-4����̉񓚂𐶐�
        generated_text = generate_text(input_prompt, role, conversation_history)
        
        # �񓚂�\��
        print("GPT-4����̉�:", generated_text)