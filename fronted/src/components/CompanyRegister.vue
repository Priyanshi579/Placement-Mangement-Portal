<template>
    <div id = "main">
        <div id = "formbody">
            <h1 Style = "text-align: center;"> Company Registeration</h1>
            <form @submit.prevent="handleCompanyregister">
                <div>
                    <label class = "mx-3 my-3" for="name">Name:</label>
                    <input type = 'text' id ="name" v-model = "form.name"  required>
                </div>
                <div>
                    <label class = "mx-3 my-3" for="location">location:</label>
                    <input type = 'text' id ="location" v-model = "form.location" required>
                </div>
                <div>
                    <label class = "mx-3 my-3" for="Contact">Contact:</label>
                    <input type = 'number' id ="Contact" v-model = "form.contact" required>
                </div>
                <div>
                    <label class = "mx-3 my-3" for="description">Despcription:</label>
                    <input type = 'text' id ="description" v-model = "form.description" required>
                </div>
                Please add at least one Despcription
                <div style = "text-align: center;">
                    <button class = "btn btn-primary me-3 mb-3" type="submit">Register</button><br>
                    <button class = "btn btn-info me-3 mb-3"  @click = "$router.push('/')">Back</button>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
    export default{
        name:'CompanyRegister',
        emits:['profile-completed','approval'],
        data(){
            return{
                form:{
                    name:'',
                    location:'',
                    contact:'',
                    description:''
                }
            }
        },
        methods:{
            async handleCompanyregister(){
                try {
                    const token = localStorage.getItem('token');
                    if(!token){
                        alert("Token not found. Please log in.");
                        return; // Stop execution if there's no token
                    }
                    
                    // FIX: Changed URL from '/api/students' to '/api/register/student'
                    const response = await axios.post('http://localhost:5000/api/register/company', this.form, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    alert("Registration successful!");
                    this.$emit('profile-completed','approval',response.data);
                    
                } catch(error) {
                    console.error('Registration failed:', error.response ? error.response.data : error.message);
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

/* #formbody{
        height: 590px;
        width :420px;
        margin-top: 132px;
    } */

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