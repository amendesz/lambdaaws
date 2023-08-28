import boto3


def lambda_handler(event, context):
    # Inicialize o cliente Lightsail
    lightsail_client = boto3.client('lightsail', region_name='us-east-2')  # Ohio (us-east-2)

    # Define as tags que você deseja usar para selecionar instâncias
    tag_key = 'dash'
    tag_value = 'homolog1'

    # Lista todas as instâncias
    response = lightsail_client.get_instances()

    for instance in response['instances']:
        instance_name = instance['name']

        # Obtenha as tags da instância
        tags = instance.get('tags', [])

        # Verifique se a instância tem a tag desejada
        for tag in tags:
            if tag['key'] == tag_key and tag['value'] == tag_value:
                # Verifique o estado atual da instância
                response = lightsail_client.get_instance_state(instanceName=instance_name)
                instance_state = response['state']['name']

                # Desligue a instância se estiver ligada
                if instance_state == 'running':
                    response = lightsail_client.stop_instance(instanceName=instance_name)
                    print(f'Instância {instance_name} desligando: {response}')
                # Ligue a instância se estiver desligada
                elif instance_state == 'stopped':
                    response = lightsail_client.start_instance(instanceName=instance_name)
                    print(f'Instância {instance_name} ligando: {response}')
                else:
                    print(f'A instância {instance_name} está em estado inválido: {instance_state}')

                break  # Sair do loop de tags se a tag for encontrada

    return 'Concluído'
