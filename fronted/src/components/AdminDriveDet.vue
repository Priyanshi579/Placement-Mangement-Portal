<template>
    <div id="main" class="d-flex justify-content-center ">
        <div id="canvas">
            <div id= "nav">
                <nav class="navbar bg-primary" data-bs-theme="dark">
                    <div class="container-fluid justify-content-between align-items-center">
                        <a class="navbar-brand  mb-0 h1" style="color:brown">Welcome to drive details page {{ drive.name }}</a>
                        <button type="button" class="btn btn-danger" @click = "logout()">logout</button>
                    </div>
                    
                </nav>
            </div>
            <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Drive Name:</h3>
                    <p style="margin: 0;">{{ drive.name }}</p>
            </div>
            <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Company Name:</h3>
                    <p style="margin: 0;">{{ company_name }}</p>
            </div>
            <div padding = "10px">
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Job Title:</h3>
                    <p style="margin: 0;">{{ drive.jobtitle }}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Job Description:</h3>
                    <p style="margin: 0;">{{ drive.jobdescription }}</p>
                </div>
                <div style = "display: flex; align-items: baseline; margin-bottom:15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Eligbility:</h3>
                    <p style="margin: 0;">{{ drive.eligbility}}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Deadline:</h3>
                    <p style="margin: 0;">{{ drive.deadline }}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">MinCgpa:</h3>
                    <p style="margin: 0;">{{ drive.min_cgpa }}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Location:</h3>
                    <p style="margin: 0;">{{ drive.location }}</p>
                </div>

                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Salary:</h3>
                    <p style="margin: 0;">{{ drive.salary }}</p>

                </div>
                <div class = "button_container">
                    <!-- <button v-if="this.role === 'student'" class="btn btn-danger" style = "margin-right: 10px; margin-left: 20px;" @click = "apply(drive.id)">Apply</button> -->
                    <button class="btn btn-primary" @click = "this.$router.push('/admin/dashboard')">Back</button>
                </div>

                
            </div>
        </div>
    </div>
        
</template>

<script>
import axios from 'axios'
export default{
    name:'AdminDriveApplieddet',
    components:{
        
    },
    data(){
        return{
            drive : {},
            company_name : '',
            role : ''
        }
    },
    async mounted() {
            try{
                const token = localStorage.getItem('token')|| localStorage.getItem('admin_token');
                if(!token){
                    alert("Token not found. Please log in.");
                    this.$router.push('/');
                    return; 
                }
                const drive_id  = this.$route.params.drive_id;
                const response = await axios.get(`http://localhost:5000/api/get/drive/${drive_id}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                this.drive = response.data.data;
                this.company_name = response.data.details.name;
                this.role = response.data.data.role;
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
    margin-top:10px;
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
