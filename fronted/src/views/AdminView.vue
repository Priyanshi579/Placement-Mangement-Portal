<template>
    <div class = "main">

        <div  v-if = "!isloggedIn">
            <AdminLogin @logged = "handleLogin" />
        </div>
        <div v-else>
            <AdminDashboard />
        </div>
    </div>
</template>
<script>
import AdminLogin from '../components/AdminLogin.vue'
import AdminDashboard from '../components/AdminDashboard.vue'

export default{
    name: "AdminView",
    components:{
        AdminLogin,
        AdminDashboard
    },
    data(){
        return{
            isloggedIn: false
        }
    },
    methods: {
        handleLogin(){
            this.isloggedIn = true
        }
    }
}
</script >

<style scoped>
    .main{
        min-height: 100vh;
        width: 100%;
        background-color: #d9f3ff;
        text-align: center;

        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
</style>