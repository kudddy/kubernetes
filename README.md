# Мануал по куберу с работающими проектами


## Как развернуть локально кластер с одним узлом?
Нужно использовать minikube. Подробный туториал лежит тут - https://kubernetes.io/ru/docs/tasks/tools/install-minikube/
все доходчико, проблем не возникло

## Основаня идея

В деплойменте описываются основные свойста будущего сервиса: ссылка на образ и переменные глобального окружения, порты, 
названия приложения и тд.
Чтобы приложение стало доступен во вне/внутри кластера нужен сервис, который опредеяет доступность приложения. 
Параметры сервиса описаны в документации
ps. примеры приложений, деплоймента и сервисов есть в папках проекта.
## Основные полезные команды minikube
```
minikube start - запуск кластеа
```
```
minikube delete - завершение работы кластера с удалением всего внутренненго состояния
```
```
minikube dashboard - запуск web формы состояния кластера
```

```
minikube service hello-node - Minikube возвращает конечную ссылк на endpoint сервиса в сети. Название сервиса - hello-node 
```

## Основные команды kubectl

Полезная ссылка со всеми командами - https://kubernetes.io/ru/docs/reference/kubectl/cheatsheet/
```
kubectl apply -f nginx-deployment.yaml - считываем деплоймент и согласно плану разворачиваем сервис
```
```
kubectl get pods - выводим развернытуе поды
```

```
kubectl get services - смотрим доступные сервисы
```

```
kubectl get events - события кластера
```

## Как добавить ELK стек в класте
Для работы кластера c ELK стеком требуется дополнительная огневая мощь.
```
minikube start --cpus 4 --memory 8192 
```

установим в кластер модули:
```
minikube addons enable storage-provisioner
```
```
minikube addons enable default-storageclass
```

# Установка HELM
```
curl https://raw.githubusercontent.com/kubernetes/Helm/master/scripts/get > get_Helm.sh
chmod 700 get_Helm.sh
./get_Helm.sh
```
На выходе:
```
Downloading https://get.Helm.sh/Helm-v2.14.3-darwin-amd64.tar.gz
Preparing to install Helm and tiller into /usr/local/bin
Helm installed into /usr/local/bin/Helm
tiller installed into /usr/local/bin/tiller
Run 'Helm init' to configure Helm.
```

Инициализаця HELM
```
Helm init
```
Смотрим запускается ли тиллер
```
kubectl get pods -n kube-system | grep tiller 
```
Выход
```
tiller-deploy-77b79fcbfc-hmqj8 1/1 Running 0 50s 
```

# Далее с помощью пакетного менеджера HELM установим в кластер ПО

Деплой Elasticsearch кластер
It’s time to start deploying the different components of the ELK Stack. Let’s start with Elasticsearch.

As mentioned above, we’ll be using Elastic’s Helm repository so let’s start with adding it:
Добавим в helm репозиторий elastic

Helm repo add elastic https://Helm.elastic.co
"elastic" has been added to your repositories

Copy
Next, download the Helm configuration for installing a multi-node Elasticsearch cluster on Minikube: 

```
curl -O https://raw.githubusercontent.com/elastic/Helm-charts/master/elasticsearch/examples/minikube/values.yaml
```
Copy
Install the Elasticsearch Helm chart using the configuration you just downloaded:
```
Helm install --name elasticsearch elastic/elasticsearch -f ./values.yaml 
```
Copy
The output you should be seeing looks something like this:
```
NAME:   elasticsearch
LAST DEPLOYED: Mon Sep 16 17:28:20 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Pod(related)
NAME                    READY  STATUS   RESTARTS  AGE
elasticsearch-master-0  0/1    Pending  0         0s

==> v1/Service
NAME                           TYPE       CLUSTER-IP     EXTERNAL-IP  PORT(S)            AGE
elasticsearch-master           ClusterIP  10.101.239.94         9200/TCP,9300/TCP  0s
elasticsearch-master-headless  ClusterIP  None                  9200/TCP,9300/TCP  0s

==> v1beta1/PodDisruptionBudget
NAME                      MIN AVAILABLE  MAX UNAVAILABLE  ALLOWED DISRUPTIONS  AGE
elasticsearch-master-pdb  N/A            1                0                    0s

==> v1beta1/StatefulSet
NAME                  READY  AGE
elasticsearch-master  0/3    0s


NOTES:
1. Watch all cluster members come up.
  $ kubectl get pods --namespace=default -l app=elasticsearch-master -w
2. Test cluster health using Helm test.
  $ Helm test elasticsearch
Copy
As noted at the end of the output, you can verify your Elasticsearch pods status with:
```
kubectl get pods --namespace=default -l app=elasticsearch-master -w 
```
Copy
It might take a minute or two, but eventually, three Elasticsearch pods will be shown as running:
```
NAME                     READY     STATUS     RESTARTS   AGE
elasticsearch-master-0   1/1       Running   0         1m
elasticsearch-master-2   1/1       Running   0         1m
elasticsearch-master-1   1/1       Running   0         1m
```
Copy
Our last step for deploying Elasticsearch is to set up port forwarding:
```
kubectl port-forward svc/elasticsearch-master 9200
```
Copy
Advanced Elasticsearch Configurations with Helm Charts
There is support for loadBalancerSourceRanges, which specifies exceptions of ranges of IP addresses that can access the designated load balancer. This is also available for Kibana.

# Deploy kibana
Next up — Kibana. As before, we’re going to use Elastic’s Helm chart for Kibana:
```
Helm install --name kibana elastic/kibana 
```
Copy
And the output: 
```
NAME:   kibana
LAST DEPLOYED: Wed Sep 18 09:52:21 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Deployment
NAME           READY  UP-TO-DATE  AVAILABLE  AGE
kibana-kibana  0/1    1           0          0s

==> v1/Pod(related)
NAME                            READY  STATUS             RESTARTS  AGE
kibana-kibana-6d7466b9b9-fbmsz  0/1    ContainerCreating  0         0s

==> v1/Service
NAME           TYPE       CLUSTER-IP    EXTERNAL-IP  PORT(S)   AGE
kibana-kibana  ClusterIP  10.96.37.129         5601/TCP  0s

Copy
Verify your Kibana pod is running (it might take a minute or two until the status turns to “Running”):

kubectl get pods

NAME                             READY     STATUS    RESTARTS   AGE
elasticsearch-master-0           1/1       Running   0          15m
elasticsearch-master-1           1/1       Running   0          15m
elasticsearch-master-2           1/1       Running   0          15m
kibana-kibana-6d7466b9b9-fbmsz   1/1       Running   0          2m
Copy
And last but not least, set up port forwarding for Kibana with: 
```
```
kubectl port-forward deployment/kibana-kibana 5601
```
Copy
You can now access Kibana from your browser at: http://localhost:5601:

# Deploy filebeat

Advanced filebeat Configurations with Helm Charts
```
helm install --name filebeat elastic/filebeat
```
and configurate this
```
kind: ConfigMap
apiVersion: v1
metadata:
  name: filebeat-filebeat-config
  namespace: default
  uid: 77b1e335-0854-4434-a58d-145f272681f1
  resourceVersion: '4573'
  creationTimestamp: '2021-01-28T13:54:04Z'
  labels:
    app: filebeat-filebeat
    chart: filebeat-7.10.2
    heritage: Tiller
    release: filebeat
  managedFields:
    - manager: Go-http-client
      operation: Update
      apiVersion: v1
      time: '2021-01-28T13:54:04Z'
      fieldsType: FieldsV1
      fieldsV1:
        'f:data': {}
        'f:metadata':
          'f:labels':
            .: {}
            'f:app': {}
            'f:chart': {}
            'f:heritage': {}
            'f:release': {}
    - manager: dashboard
      operation: Update
      apiVersion: v1
      time: '2021-01-28T14:58:14Z'
      fieldsType: FieldsV1
      fieldsV1:
        'f:data':
          'f:filebeat.yml': {}
data:
  filebeat.yml: |
    filebeat.autodiscover:
      providers:
        - type: kubernetes
          templates:
            - condition:
                equals:
                  kubernetes.container.name: flask-frontend
              config:
                - type: container
                  paths:
                    - /var/log/containers/*-${data.kubernetes.container.id}.log
    # filebeat.inputs:
    # - type: container
    #   paths:
    #     - /var/log/containers/*.log
    #   processors:
    #   - add_kubernetes_metadata:
    #       host: ${NODE_NAME}
    #       matchers:
    #       - logs_path:
    #           logs_path: "/var/log/containers/"

    output.elasticsearch:
      host: '${NODE_NAME}'
      hosts: '${ELASTICSEARCH_HOSTS:elasticsearch-master:9200}'
```
P.S, чтобы все логи не сыпались с разные контейнеров нужно написть условия для filebeat
Побробнее тут: https://www.elastic.co/guide/en/beats/filebeat/current/configuration-autodiscover.html
# Summary

we deploy elk stack 