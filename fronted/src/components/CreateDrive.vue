<template>
    <div id = "main">
        <div id = "formbody">
            <form @submit.prevent="CreateDrive">
                <div v-if = "errorMessage">
                    <h1>  {{errorMessage}}</h1>
                </div>
                <div v-else>
                    <h1 Style = "text-align: center;">Create Drive form</h1>
                    <div class="mb-3">
                        <label for="name"> Drive name:</label>
                        <input type = 'text' id ="name" v-model = "form.name"  required>
                    </div>
                    <div class="mb-3">
                        <label for="job tiltle">Job title:</label>
                        <input type = 'text' id ="jobtitle" v-model = "form.jobtitle" required>
                    </div>
                    <div class="mb-3">
                        <label for="description">Description:</label>
                        <input type = 'text' id ="description" v-model = "form.description" required>
                    </div> 
                    <div class="mb-3">
                        <label for="Eligbility">Eligbility Criteria:</label>
                        <input type = 'text' id ="Eligbility" v-model = "form.eligbility" required>
                    </div> 
                    <div class="mb-3">
                        <label for="deadline">deadline:</label>
                        <input type = 'date' id ="deadline" v-model = "form.deadline" :min="today" required>
                    </div> 
                    <div class="mb-3">
                        <label for="min_cgpa">Minimum cgpa:</label>
                        <input type = 'number' id ="min_cgpa" v-model = "form.min_cgpa" required>
                    </div> 
                    <div class="mb-3">
                        <label for="salary_package">Salary package:</label>
                        <input type = 'number' id ="salary_package" v-model = "form.salary" required>
                    </div>
                    <div class="mb-3">
                        <label for="location">Location:</label>
                        <input type = 'text' id ="location" v-model = "form.location" required>
                    </div>
                    <div class = "text-center">
                        <button class = "btn btn-primary my-1" type="submit">Save</button><br>
                        <button class = "btn btn-info my-1" @click = "$router.push('/company/dashboard') ">Back</button>

                    </div>
                </div>
            </form>
            <!-- <button class="btn btn-primary" style = "margin-right: 10px; margin-left: 20px;" @click = "goback()">Go Back</button> -->
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default{
    name:'CreateDrive',
    emits:['createdrive'],
    data(){
        return{
            form:{
                name:'',
                jobtitle:'',
                description:'',
                eligbility:'',
                deadline:'',
                min_cgpa:0,
                salary:0,
                location:''
            },
            errorMessage: ''
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
    methods: {
        async CreateDrive(){
            try{
                const token = localStorage.getItem('token');
                const response = await axios.post('http://localhost:5000/api/create/drive',this.form,{
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                })
                alert("Drive created successfully")
                console.log('response') 
                this.$emit('createdrive');
                this.$router.push('/company/dashboard');
                this.form.name = '';
                this.form.jobtitle = '';
                this.form.description = '';
                this.form.eligbility = '';
                this.form.deadline = '';
                this.form.min_cgpa = 0;
                this.form.salary = 0;
                this.form.location = '';
            }
            catch(error){
                console.log('CREATION failed', error)

                if (error.response && error.response.data && error.response.data.message) {
                this.errorMessage = error.response.data.message;
                } else {
                this.errorMessage = "Something went wrong. Please try again.";
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
        
        background-color:#d9f3ff;

        display:flex;
        justify-content:center;
        align-items:flex-start;
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
        text-align: center;

    }


</style>