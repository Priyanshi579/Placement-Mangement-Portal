<template>
    <div id="main" class="d-flex justify-content-center">
        <div id="canvas">
            <div id= "nav">
                <nav class="navbar bg-primary" data-bs-theme="dark">
                    <div class="container-fluid justify-content-between align-items-center">
                        <a class="navbar-brand  mb-0 h1" style="color:brown">Welcome to Student details page </a>
                        <button type="button" class="btn btn-danger" @click = "logout()">logout</button>
                    </div>
                    
                </nav>
            </div>
            <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Student Name:</h3>
                    <p style="margin: 0;">{{ drive.student_name }}</p>
            </div>
            <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Drive Name:</h3>
                    <p style="margin: 0;">{{ drive.drive_name }}</p>
            </div>
            <div padding = "10px">
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Job Title:</h3>
                    <p style="margin: 0;">{{ drive.jobtitle }}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Branch:</h3>
                    <p style="margin: 0;">{{ drive.branch }}</p>
                </div>
                <div style = "display: flex; align-items: baseline; margin-bottom:15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Status:</h3>
                    <p style="margin: 0;">{{ drive.status}}</p>
                </div>
                <div class = "button_container">
                    <button class="btn btn-primary" @click = "this.$router.push('/admin/dashboard')">Back</button>
                </div>

                
            </div>
        </div>
    </div>
        
</template>

<script>
import axios from 'axios'
export default{
    name:'StudentDetails',
    components:{
        
    },
    data(){
        return{
            drive : {}
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
                const application_id  = this.$route.params.id;
                const response = await axios.get(`http://localhost:5000/api/get/student/${application_id}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                this.drive = response.data;
            } catch (error){
                console.log("Some error occured : ", error);
            }
        },
    methods:{
        logout(){
            localStorage.removeItem('token');
            this.$router.push('/');

        },
        async apply(drive_id){
            try{
                const token = localStorage.getItem('token');
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
