<template>
    <div id = "main">
        <div id = "formbody">
            <h1 Style = "text-align: center;">Update Drive</h1>
            <form @submit.prevent="handleUpdateDrive">
                <div v-if = "errorMessage">
                    <h1> Something went wrong: {{errorMessage}}</h1>
                </div>
                <div v-else>
                        <div>
                            <label  class = "mx-3 my-3" for="email">Name:</label>
                            <input type='text' id="email" v-model="form.name" required>
                        </div>
                    <div>
                        <label class = "mx-3 my-3 " for="branch">Job Title:</label>
                        <input type = 'text' id ="branch" v-model = "form.jobtitle" required disabled >
                    </div>
                    <div>
                        <label class = "mx-3 my-3 " for="year">Job Description:</label>
                        <input type = 'text' id ="Year" v-model = "form.jobdescription" required disabled>
                    </div>
                    <div>
                        <label class = "mx-3 my-3 " for="cgpa"> Min Cgpa:</label>
                        <input type = "number" id ="cgpa" v-model = "form.cgpa" required>
                    </div>
                    <div>
                        <label class = "mx-3 my-3 " for="phone">Eligibility Criteria:</label>
                        <input type = 'text' id ="phone" v-model = "form.eligbility" required disabled>
                    </div>
                    <div>
                        <label class = "mx-3 my-3 " for="skills">Salary Package:</label>
                        <input type = 'text' id ="skills" v-model = "form.salary" required disabled>
                        
                    </div>
                    <div>
                        <label class = "mx-3 my-3 " for="skills">Location:</label>
                        <input type = 'text' id ="skills" v-model = "form.location" required disabled>
                        
                    </div>
                    <div>
                        <label class = "mx-3 my-3 " for="deadline">Deadline:</label>
                        <input type = 'date' id ="skills" v-model = "form.deadline" :min="today" required >

                        
                    </div>
                    <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                        <h9 style="margin: 0; margin-left: 20px; margin-right: 15px; ">choose Status:</h9>
                        <select  v-model="form.status" class="form-select form-select-sm" aria-label="Small select example">
                            <option selected value="" disabled>Open this select menu</option>
                            <option value="Pending">Pending</option>
                            <option value="Completed">Completed</option>
                        </select>

                    </div>
                    <div Style = "text-align: center;">
                        <button class = "btn btn-primary me-3 mb-3 "type="submit">Update</button><br>
                        <button class = "btn btn-info me-3 mb-3 "type="submit" @click = "this.$router.push('/company/dashboard')">Back</button>
                    </div>

                </div>
        
            </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
    export default{
        name:'UpdateDrive',
        
        data(){
            return{
                form:{
                    name:'',
                    jobtitle:'',
                    jobdescription:'',
                    eligbility:'',
                    deadline:'',
                    salary:0,
                    location:'',
                    status:'',
                    'cgpa':0
                },
                errorMessage: '',
                
            }
        },
        async mounted() {
            try{
                const token = localStorage.getItem('token');
                if(!token){
                    alert("Token not found. Please log in.");
                    return; // Stop execution if there's no token
                }
                const drive_id  = this.$route.params.drive_id;
                const response = await axios.get(`http://localhost:5000/api/get/drive/${drive_id}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                const drive = response.data.data;
                this.form.name = drive.name;
                this.form.jobtitle = drive.jobtitle;
                this.form.jobdescription = drive.description;
                this.form.eligbility = drive.eligbility;
                this.form.deadline = drive.deadline;
                this.form.salary = drive.salary;
                this.form.location = drive.location;
                this.form.cgpa = drive.min_cgpa;
                this.form.status = drive.status;
                

            } catch (error){
                console.log("No preious profile found, please register");
            }
        },
        computed: {
        today(){
            const now = new Date();
            const year = now.getFullYear();
            // Months are 0-indexed in JS, so add 1. padStart ensures 2 digits (e.g., '06')
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        }
    },
        // Inside your Vue Component <script> tag:
        methods: {
            async handleUpdateDrive(){
                try {
                    const token = localStorage.getItem('token');
                    if(!token){
                        alert("Token not found. Please log in.");
                        return; // Stop execution if there's no token
                    }
                    
                    const drive_id = this.$route.params.drive_id;
                    const response = await axios.put(`http://localhost:5000/api/update/drive/${drive_id}`, 
                    {
                        name: this.form.name,
                        jobtitle: this.form.jobtitle,
                        description: this.form.jobdescription,
                        eligbility: this.form.eligbility,
                        min_cgpa: this.form.cgpa,
                        salary: this.form.salary,
                        location: this.form.location,
                        deadline: this.form.deadline,
                        status: this.form.status
                    }, 
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    alert("drive updated successfully!");
                    this.$router.push("/company/dashboard")
                    
                } catch(error) {
                    console.error('Registration failed:', error.response ? error.response.data : error.message);
                    if (error.response && error.response.data && error.response.data.message) {
                    this.errorMessage = error.response.data.message;
                    } else {
                    this.errorMessage = "Something went wrong. Please try again.";
                    }
                    alert("Registration failed. Please check the console for details.");
                }
            }
        }
    }
</script>
<style scoped>
*{
    margin:0px;
}



#main{
    min-height: 100vh;
    background-color: #d9f3ff;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: 40px;
    }
#canvas{
    margin: auto;
    height: 800px;
    width:60%;
    border:2px solid white;
}
#formbody{
        width: 500px;
        border: 9px solid gray;
        border-radius: 5px;
        padding: 10px;
        margin: 0;
        height: auto;
    }
#Table{
    padding: 8px;
    margin-top: 1px;
}
</style>