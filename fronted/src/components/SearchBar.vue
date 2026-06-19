<template>
    <div id="main" class="d-flex justify-content-center">
        <div id="canvas">
            <div id= "nav">
                <nav class="navbar bg-primary" data-bs-theme="dark">
                    <div class="container-fluid justify-content-between align-items-center">
                        <a class="navbar-brand  mb-0 h1" style="color:brown">Welcome Admin</a>
                        <button type="button" class="btn btn-danger" @click = "logout()">logout</button>
                    </div>
                    
                </nav>
            </div>
            <h1 style = "text-align: center;">Searched result</h1>
            <div v-if = "data.role == 'student'" >
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;"> StudentName:</h3>
                        <p style="margin: 0;">{{ data.name }}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Contact No:</h3>
                        <p style="margin: 0;">{{ data.phone }}</p>
                </div>
                <div padding = "10px">
                    <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Branch:</h3>
                        <p style="margin: 0;">{{ data.branch }}</p>
                    </div>
                    <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Passing Year:</h3>
                        <p style="margin: 0;">{{ data.year }}</p>
                    </div>
                    <div style = "display: flex; align-items: baseline; margin-bottom:15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Cgpa:</h3>
                        <p style="margin: 0;">{{ data.cgpa}}</p>
                    </div>
                    <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Skills:</h3>
                        <p style="margin: 0;">{{ data.skills }}</p>
                    </div>
                    <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Email:</h3>
                        <p style="margin: 0;">{{ data.email }}</p>
                    </div>
                </div>
            </div>
            <div v-else-if = "data.role == 'company'">
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Company Name:</h3>
                        <p style="margin: 0;">{{ data.name }}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Contact No:</h3>
                        <p style="margin: 0;">{{ data.phone }}</p>
                </div>
                <div padding = "10px">
                    <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Email:</h3>
                        <p style="margin: 0;">{{ data.email}}</p>
                    </div>
                    <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Job Description:</h3>
                        <p style="margin: 0;">{{ data.description }}</p>
                    </div>
                    <div style = "display: flex; align-items: baseline; margin-bottom:15px;">
                        <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Location:</h3>
                        <p style="margin: 0;">{{ data.location}}</p>
                    </div>

                </div>
            </div>
            <div class = "button_container">
                    <button class="btn btn-primary" @click = "this.$router.push('/admin/dashboard')">Back</button>
            </div>
        </div>
    </div>
        
</template>

<script>
import axios from 'axios'
export default{
    name:'SearchBar',
    components:{
        
    },
    data(){
        return{
            data : {},
            errorMessage: '',
        }
    },
    async mounted() {
            try{
                const token = localStorage.getItem('admin_token');
                if(!token){
                    alert("Token not found. Please log in.");
                    this.$router.push('/');
                    return; 
                }
                const user_type = this.$route.params.user_type;
                const search = this.$route.params.search;
                const response = await axios.get(`http://localhost:5000/api/search/${user_type}/${search}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                console.log("Search response:", response.data);
                this.data = response.data;
                
            } catch (error){
                console.log("Some error occured : ", error);
            }
        },
    methods:{
        logout(){
            localStorage.removeItem('admin_token');
            this.$router.push('/');

        },
        async apply(drive_id){
            try{
                const token = localStorage.getItem('admin_token');
                const response = await axios.post(`http://localhost:5000/api/apply/${drive_id}`, {}, {
                    headers:{
                        'Conten-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                alert("Applied Successfully");
            }catch (error) {
                console.error('Apply system error layout:', error);
                if (error.response && error.response.data) {
                    console.log("Flask Backend Error Data:", error.response.data);
                    alert(error.response.data.message); 
                } else {
                    console.log("Network/Server is unreachable:", error.message);
                    alert("Network error: Could not reach the server.");
                }
            }
                
        }
    }
}
</script>

<style scoped>
#main{
    width:100%;
    min-height:100vh;
    /* margin-top:10px; */
    background-color:#d9f3ff;

    display:flex;
    justify-content:center;
    align-items:flex-start;
}

#canvas{
    /* margin: auto; */
    height: 800px;
    width:60%;
    border:2px solid white;
}
#formbody{
    border:9px solid gray;
    width :300px;
    height:400px;
    margin: auto;
    border-radius: 5px;
    margin-top: 200px;
    padding:10px;
}
#Table{
    padding: 8px;
    margin-top: 1px;
}
.button_container{
    display: flex;
    justify-content: center; 
    align-items: center;     /* VERTICAL ALIGNMENT: Perfectly aligns the shapes vertically */
    gap: 15px;               /* SPACE BETWEEN BUTTONS: Injects clean spacing between Apply and Back */
    margin-top: 35px;        /* Moves buttons down away from the dataset rows */
    margin-bottom: 20px;
}

</style>
