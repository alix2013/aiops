oc create -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-share-pvc
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 20Gi
EOF


#failed, unable to add it for running pod 
#oc set volume pod/testm --add --name=sharevol --claim-name=my-share-pvc --mount-path=/data


oc create -f - << EOF 
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu1
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command: ["tail", "-f", "/dev/null"]
    volumeMounts:
    - name: my-volume
      mountPath: /data
  volumes:
  - name: my-volume
    persistentVolumeClaim:
      claimName: my-share-pvc
EOF


oc create -f - << EOF 
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu2
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command: ["tail", "-f", "/dev/null"]
    volumeMounts:
    - name: my-volume
      mountPath: /data
  volumes:
  - name: my-volume
    persistentVolumeClaim:
      claimName: my-share-pvc
EOF




