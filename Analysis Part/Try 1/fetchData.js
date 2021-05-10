
  var firebaseConfig = {
    apiKey: "AIzaSyBIrvPerFGU6BdsFFucfnYbXRcd8EcOzHk",
    authDomain: "iot-project-1fc52.firebaseapp.com",
    databaseURL: "https://iot-project-1fc52-default-rtdb.firebaseio.com",
    projectId: "iot-project-1fc52",
    storageBucket: "iot-project-1fc52.appspot.com",
    messagingSenderId: "216918432114",
    appId: "1:216918432114:web:f46429cc31fac6fc0ce5eb",
    measurementId: "G-VC1D400YJE"
  };
  var json_data=[]
  firebase.initializeApp(firebaseConfig);
  const database=firebase.database();
    database.ref('Observations').once('value',function(snapshot){
        
        snapshot.forEach(
            function(ChildSnapshot)
            {
                json_data.push({ index:ChildSnapshot.val().index,
                    lat:ChildSnapshot.val().lat,
                    longi:ChildSnapshot.val().longi,
                    x:ChildSnapshot.val().x,
                    y:ChildSnapshot.val().y,
                    z:ChildSnapshot.val().z,
                })
                
            }
        )
    });
    console.log(json_data)
    //console.log($.csv.fromObjects());
    //console.log(file1)
    const downloadToFile = (content, filename, contentType) => {
        const a = document.createElement('a');
        const file = new Blob([JSON.stringify(json_data, null, 2)], {type : 'application/json'});
        
        a.href= URL.createObjectURL(file);
        a.download = filename;
        a.click();
      
          URL.revokeObjectURL(a.href);
      };
      
      document.querySelector('#btnSave').addEventListener('click', () => {
        
        downloadToFile(json_data, 'my-new-file.json', 'text/plain');
      });
