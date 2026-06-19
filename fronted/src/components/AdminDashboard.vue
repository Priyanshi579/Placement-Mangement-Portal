<template>
    <div id="main" class="d-flex justify-content-center  ">
        <div id="canvas">
            <div id= "nav">
                <nav class="navbar bg-primary" data-bs-theme="dark">
                    <div class="container-fluid">
                        <a class="navbar-brand" style="color:brown">Welcome Admin</a>
                        <form class="d-flex" @submit.prevent="search">
                            <select  v-model = "user_type" class="form-select" aria-label="Default select example" >
                                <option value = "" selected disabled >Open this select menu</option>
                                <option value="company">Company</option>
                                <option value="student">Student</option>
                            </select>
                            <input v-model ="search_query" class="form-control me-2" type="search" placeholder="Enter name of student or organisation" aria-label="Search" />
                            <button class="btn btn-outline-success" >Search</button>
                        </form>
                    </div>
                </nav>
                <br>
                <div id="content" class="px-2">
                    <header class="d-flex justify-content-end mb-4">
                        <button type="button" class="btn btn-outline-danger me-2" @click = "logout()">logout</button>
                        <button type="button" class="btn btn-outline-info" @click = "this.$router.push('/')">Back</button>
                    </header>
                </div>
                <div class="px-2">
                    <nav class="d-flex flex-column">
                        <button class="btn btn-primary" @click = "active = 'student'">Student</button>
                        <br><br><AdminStudent v-if = "active === 'student'"></AdminStudent>
                        <button class="btn btn-primary" @click = "active = 'company'">Registered Company</button>
                        <br><br><AdminCompany v-if = "active === 'company'"></AdminCompany>
                        <button class="btn btn-primary" @click = "active = 'ongoing'">Ongoing Company</button>
                        <br><br><OngoingCompany v-if = "active === 'ongoing'"></OngoingCompany>
                        <button class="btn btn-primary" @click = "active = 'application'">Student Application</button>
                        <br><br><StudentApplication v-if = "active === 'application'"></StudentApplication>
                        <button class="btn btn-primary" @click = "active = 'drive'">Drive</button>
                        <br><br><AdminDrive v-if = "active === 'drive'"></AdminDrive>
                        <button class="btn btn-primary" @click = "active = 'summary'">Summary</button>
                        <AdminSummary v-if = "active === 'summary'"></AdminSummary>
                    </nav>
                </div>
                <!-- <div>
                    <main>
                        <AdminStudent v-if = "active === 'student'"></AdminStudent>
                        <AdminCompany v-if = "active === 'company'"></AdminCompany>
                        <OngoingCompany v-if = "active === 'ongoing'"></OngoingCompany>
                        <StudentApplication v-if = "active === 'application'"></StudentApplication>
                        <AdminDrive v-if = "active === 'drive'"></AdminDrive>
                        <AdminSummary v-if = "active === 'summary'"></AdminSummary>
                    </main>
                </div> -->
            </div>
        </div>
    </div>
        
</template>

<script>
import AdminStudent from '../components/AdminStudent.vue'
import AdminCompany from '../components/AdminCompany.vue'
import OngoingCompany from '../components/OngoingCompany.vue'
import StudentApplication from '../components/StudentApplication.vue'
import AdminDrive from '../components/AdminDrive.vue'
import AdminSummary from '../components/AdminSummary.vue'
export default{
    name:'AdminDashboard',
    components:{
        AdminStudent,
        AdminCompany,
        OngoingCompany,
        StudentApplication,
        AdminDrive,
        AdminSummary
        
    },
    data(){
        return{
            active:'hii',
            search_query: '',
            user_type: ''
        }
    },
    methods:{
        logout(){
            localStorage.removeItem('admin_token');
            this.$router.push('/');

        },
        search(){
            this.$router.push({name:'SearchBar', params:{user_type:this.user_type, search:this.search_query}});
        },

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
    padding-top:10px;
}

#canvas{
  width:700px;
  min-height:100vh;
  border:2px solid white;
  background-color:#d9f3ff;
}
html, body, #app {
  margin: 0;
  min-height: 100vh;
  background-color: #d9f3ff;
}

#formbody{
    border:9px solid #d9f3ff;
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

</style>
