<template>
    <div id = "main">
        <div id = "formbody">
            <form @submit.prevent="handleregister">
                <h1 Style = "text-align: center;">Register form</h1>
                <br>
                <div class="mb-3">
                    <label for="username">Username:</label>
                    <input type = 'text' id ="username" v-model = "form.username"  required>
                </div>
                <div class="mb-3">
                    <label for="email">Email:</label>
                    <input type = 'text' id ="email" v-model = "form.email" required>
                </div>
                <div class="mb-3">
                    <label for="password">Password:</label>
                    <input type = 'text' id ="password" v-model = "form.password" required>
                </div> 
                <div class="mb-3">
                    <label for="role">Role:</label>
                    <select id = "role" class="form-select" aria-label="Default select example" v-model = "form.role">
                        <option disabled value = "">select the role</option>
                        <option value="admin">Admin</option>
                        <option value="student">Student</option>
                        <option value="company">Company</option>
                    </select>
                </div>
                <div class = "text-center">
                    <button class = "btn btn-primary mb-3" type="submit">Register</button><br>
                    <a  href = "#" @click.prevent="$emit('login-here')">Already have an account ? Login</a>
                </div>
                <!-- <a  href = "#" @click.prevent="$emit('login-here')">Already have an account ? Login</a> -->
            </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
    export default{
        name:'UserRegister',
        emits:['register','login-here'  ],
        data(){
            return{
                form:{
                    username:'',
                    email:'',
                    password:'',
                    role:''
                }
            }
        },
        methods: {
            async handleregister(){
                try{
                    const response = await fetch('http://localhost:5000/api/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.form)
                })
                const data = await response.json()

                if (!response.ok) {
                    alert(data.message)
                    return
                }
                alert(data.message)
                this.$emit('register')
            }
            catch(error){
                console.log('Register failed', error)
                alert(error.message)
            }
            }
                
        }   
    }

</script>
<style scoped>
    #formbody{
        height: 590px;
        width :420px;
        margin-top: 51px;
        
    }
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
        border:9px solid gray;
        width :420px;
        height:400px;
        margin: auto;
        border-radius: 5px;
        margin-top: 51px;
        padding:20px;
    }
</style>
