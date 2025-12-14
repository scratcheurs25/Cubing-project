const USER_URL = "http://127.0.0.1:5000/api/v0/user/";
const EVENT_URL = "http://127.0.0.1:5000/api/v0/event/";
const GROUP_URL = "http://127.0.0.1:5000/api/v0/group/"
const ROOT_URL = "http://127.0.0.1:5000/"
const RESULT_URL = "http://127.0.0.1:5000/api/v0/result/"

let username = document.getElementById("username")
let password = document.getElementById("password")
let user = document.getElementById("id")
let event = document.getElementById("idevent")
let icon = document.getElementById("icon")
let rule = document.getElementById("text")
let name_group = document.getElementById("name_group")

function make_cookie(cookie,value){
    document.cookie = `${cookie}=${value}; Max-Age=86400; path=/`;
}


 async function create_user() {

    //let string_bool = role.checked ? "true" : "false";
      const payload = {
         "args":[username.value,"",password.value,
         false,icon.value]
      };

      // Requête POST vers ton API Flask
      const response = await fetch(USER_URL+"add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      alert(data)
    }

    async function del_user(ID) {

      const payload = { 
         "args":[ID]
      };

      // Requête POST vers ton API Flask
      const response = await fetch(USER_URL+"remove", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      alert(data)
    }

    async function get_all_users() {

      const payload = { 
         "args":[]
      };

      // Requête POST vers ton API Flask
      const response = await fetch(USER_URL+"get_all", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      const message = data.map(user => `ID: ${user.id} : ${user.name}`).join(" , ");
      alert(message)
    }
    async function get_user(ID) {

      const payload = {
         "args":[ID]
      };

      // Requête POST vers ton API Flask
      const response = await fetch(USER_URL+"get", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      const message = data.map(user => `ID: ${user.id} : ${user.name} , ${user.wca} ,${user.password},${user.role},,${user.icon} `).join(" , ");
      return(data)
    }
    async function connect() {
  const payload = {
    "args": [username.value, password.value]
  };

  try {
    // Envoi de la requête POST vers ton API Flask
    const response = await fetch(USER_URL + "connect", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload),
      credentials: "include"   // 🔑 très important pour que le cookie de session soit envoyé
    });

    const data = await response.json();

    // Vérifie si la connexion est réussie
    if (data && data.logged_in) {
      // Redirige vers la route Flask qui sert index.html
      window.location.replace("http://127.0.0.1:5000/index");
    } else {
      alert("Nom d'utilisateur ou mot de passe incorrect");
    }
  } catch (error) {
    console.error("Erreur lors de la connexion :", error);
    alert("Impossible de se connecter au serveur");
  }
}
async function verif(){
  const response = await fetch(ROOT_URL+"get", {
      method: "GET",
    });
  const data = await response.json();

    // Vérifie si la connexion est réussie
    if (data && !data.logged_in) {
      // Redirige vers la route Flask qui sert index.html
      window.location.replace("http://127.0.0.1:5000/login");
    }

}

async function get_curent_user() {
  const response = await fetch(ROOT_URL+"get", {
    method: "GET",
    credentials: "include"   // 🔑 pour que le cookie de session soit envoyé
  });

  const data = await response.json();
  return (data.user_id)
}

async  function get_all_event(){
    const payload = {
         "args":[]
      };

      // Requête POST vers ton API Flask
      const response = await fetch(EVENT_URL+"get_all", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      const message = data.map(event => `ID: ${event.id} : ${event.name}`).join(" , ");
      return data
}

async  function get_event(ID){
    const payload = {
         "args":[ID]
      };

      // Requête POST vers ton API Flask
      const response = await fetch(EVENT_URL+"get", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      const message = data.map(event => `ID: ${event.id} : ${event.name}`).join(" , ");
      return data
}

async function create_events(){
      const payload = {
         "args":[username.value,icon.value, await get_curent_user() , rule.value]
      };
      alert("complete")
      // Requête POST vers ton API Flask
      const response = await fetch(EVENT_URL+"add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      alert(data)
}

async function delete_event(id){
      const payload = {
         "args":[id]
      };
      if (confirm("Voulez-vous supprimer cet événement ?")) {
          // Requête POST vers ton API Flask
          const response = await fetch(EVENT_URL + "remove", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify(payload)
          });

          // Récupération de la réponse JSON
          const data = await response.json();

          window.location.href = data.redirect;
      }
}



async function editEvents(id){
    const payload = {
         "args":[id ,username.value, icon.value, rule.value]
      };
      const response = await fetch(EVENT_URL+"edit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
}

async function editProfile(){
    const payload = {
         "args":[username.value , rule.value , password.value , icon.value]
      };
      const response = await fetch(USER_URL+"edit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
}

async function get_all_group(){
    const payload = {
         "args":[]
      };
      const response = await fetch(GROUP_URL+"get_all", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      return data
}

async function get_all_user_from_group(id){
    const payload = {
         "args":[id]
      };
      const response = await fetch(GROUP_URL+"get_all_user_from_group", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      return data

}

async function get_all_events_from_group(id){
    const payload = {
         "args":[id]
      };
      const response = await fetch(GROUP_URL+"get_all_event_from_group", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      return data

}

async function add_user_to_group(id){
    const payload = {
         "args":[id,user.value]
      };
      const response = await fetch(GROUP_URL+"add_user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      return data

}

async function add_event_to_group(id){
    const payload = {
         "args":[id,event.value]
      };
      const response = await fetch(GROUP_URL+"add_event", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      return data

}

async function create_group(){
    const payload = {
         "args":[username.value , icon.value]
      };
      const response = await fetch(GROUP_URL+"add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      return data

}
async function edit_group(Id){
    const payload = {
         "args":[Id , name_group.value , icon.value]
      };
      const response = await fetch(GROUP_URL+"edit_group", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      return data

}

async function get_result_user(event,user) {
  const payload = {
         "args":[event , user]
      };
      const response = await fetch(RESULT_URL+"get_user_result", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      return data
  
}

async function get_result_user_best(event,user) {
  const payload = {
         "args":[event , user]
      };
      const response = await fetch(RESULT_URL+"get_user_best_result", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      return data

}

async function get_result_group(event,group) {
  const payload = {
         "args":[event , group]
      };
      const response = await fetch(RESULT_URL+"get_group_result", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      // Récupération de la réponse JSON
      const data = await response.json();
      return data

}

function msToMinSecMs(ms) {
    // Validation d'entrée
    if (typeof ms !== 'number' || isNaN(ms) || ms < 0) {
        throw new Error("Veuillez fournir un nombre positif en millisecondes.");
    }

    const minutes = Math.floor(ms / 60000); // 1 min = 60 000 ms
    const seconds = Math.floor((ms % 60000) / 1000);
    const milliseconds = ms % 1000;

    // Formatage avec zéro devant si nécessaire
    const secStr = seconds.toString().padStart(2, '0');
    const msStr = milliseconds.toString().padStart(3, '0');

    return `${minutes}:${secStr}:${msStr}`;
}
