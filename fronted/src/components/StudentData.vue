<template>
    <div id="main" class="d-flex justify-content-center ">
        <div id="canvas">
            <div id= "nav">
                <nav class="navbar bg-primary" data-bs-theme="dark">
                    <div class="container-fluid justify-content-between align-items-center">
                        <a class="navbar-brand  mb-0 h1" style="color:brown">Student Application </a>
                        <button type="button" class="btn btn-danger" @click = "logout()">logout</button>
                    </div>
                    
                </nav>
            </div>
            <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Student Name:</h3>
                    <p style="margin: 0;">{{ student.student_name }}</p>
            </div>
            <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Drive Name:</h3>
                    <p style="margin: 0;">{{ student.drive_name }}</p>
            </div>
            <div padding = "10px">
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Job Title:</h3>
                    <p style="margin: 0;">{{ student.jobtitle }}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Student Branch:</h3>
                    <p style="margin: 0;">{{ student.branch }}</p>
                </div>
                <div style = "display: flex; align-items: baseline; margin-bottom:15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Cgpa:</h3>
                    <p style="margin: 0;">{{ student.cgpa}}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Passing Year:</h3>
                    <p style="margin: 0;">{{ student.passing_year }}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Phone:</h3>
                    <p style="margin: 0;">{{ student.phone }}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Skills:</h3>
                    <p style="margin: 0;">{{ student.skills }}</p>
                </div>
                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">Email:</h3>
                    <p style="margin: 0;">{{ student.email }}</p>
                </div>

                <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                    <h3 style="margin: 0; margin-left: 20px; margin-right: 15px; color: #0d6efd;">choose Result:</h3>
                    <select  v-model="selected_status" class="form-select form-select-sm" aria-label="Small select example">
                        <option selected value="" disabled>Open this select menu</option>
                        <option value="shortlisted">Shortlisted</option>
                        <option value="waiting">Waiting</option>
                        <option value="rejected">Rejected</option>
                    </select>

                </div>
                <div class = "button_container">
                    <button class="btn btn-danger" style = "margin-right: 10px; margin-left: 20px;" @click = "Update_status()">Save</button>
                    <button class="btn btn-primary" @click = "$router.go(-1)">Back</button>
                </div>

                
            </div>
        </div>
    </div>
        
</template>

<script>
import axios from 'axios'
export default{
    name:'StudnetData',
    components:{
        
    },
    data(){
        return{
            student : {},
            selected_status : '',
            // company_name : ''
        }
    },
    async mounted() {
            try{
                const token = localStorage.getItem('token');
                if(!token){
                    alert("Token not found. Please log in.");
                    this.$router.push('/');
                    return; 
                }
                const student_id  = this.$route.params.student_id;
                const drive_id  = this.$route.params.drive_id;
                

                const response = await axios.get(`http://localhost:5000/api/get/student_data/${student_id}/${drive_id}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                this.student = response.data;
                
            } catch (error){
                console.log("Some error occured : ", error);
            }
        },
    methods:{
        logout(){
            localStorage.removeItem('token');
            this.$router.push('/');

        },
        async Update_status(){
            try{
                const token = localStorage.getItem('token');
                const student_id  = this.$route.params.student_id;
                const drive_id  = this.$route.params.drive_id;
                if (!this.selected_status) {
                    alert("Please select a status. before clicking save");
                    return;
                }
                const response = await axios.put(`http://localhost:5000/api/update/application_status/${student_id}/${drive_id}`, {
                    status : this.selected_status,
                    student_id : student_id,
                    drive_id : drive_id
                }, {
                    headers:{
                        'Conten-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                alert("Updated Successfully");
                this.$router.go(-1);
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
