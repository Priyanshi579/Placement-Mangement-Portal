<template>
    <div>
        <div v-if = "!isLoggedIn">
            <UserLogin v-if = "!showRegister" @logged = "handleLogin" @register-here = "showRegister = true" />
            <div v-else>
                <UserRegister v-if = "registrationStep === 1" @register = "go_loginpage" @login-here = "showRegister = false"/>
            </div>
        </div>
        <div v-else>
            <div v-if = "userRole.toLowerCase() ==='student'">
                <StudentRegister v-if = "registrationStep ===2" @profile-completed = "registrationStep = 1"/> 

                <StudentDashboard v-else :logged_student="currentStudent"/>
            </div>

            <div v-else-if = "userRole && userRole.toLowerCase() === 'company'">
                <CompanyRegister v-if = "registrationStep ===2" @profile-completed = "registrationStep = 3"/> 
                <NotApproved v-else-if = "registrationStep === 3" />
                <CompanyDashboard v-else-if = "registrationStep === 1 && approval_status === 'Approved'" :logged_company="currentCompany"/>
            </div>

            <!-- <div v-else-if = "userRole && userRole.toLowerCase() === 'admin'">
                <AdminDashboard />
            </div> -->

            <h1 v-else> Role not defined</h1>

        </div>
    </div>
</template>
<script>
import UserLogin from '../components/UserLogin.vue' 
import UserRegister from '../components/UserRegister.vue'
import StudentDashboard from '../components/StudentDashboard.vue'
import CompanyDashboard from '../components/CompanyDashboard.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import StudentRegister from '../components/StudentRegister.vue'
import CompanyRegister from '../components/CompanyRegister.vue'
import NotApproved from '../components/NotApproved.vue'
export default {
    name: 'UserView',
    components: {
        UserRegister,
        UserLogin,
        StudentDashboard,
        CompanyDashboard,
        AdminDashboard,
        StudentRegister,
        CompanyRegister,
        NotApproved

    },
    data() {
        return {
        isLoggedIn : false,
        showRegister:false,
        userRole: '',
        registrationStep: 1,
        currentCompany: '',
        currentStudent: '',
        approval_status: ''
        }
    },
    methods:{
        // handleRegistration(role){
        //     if (role){
        //         this.userRole = role, 
        //         this.registrationStep = 2 
        //     }
        // },
        handleLogin(login){
            this.isLoggedIn = true;
            this.userRole = login.role;
            this.currentCompany = login.username

            if (login.role.toLowerCase() === 'student') {
                this.currentStudent = login.username;
                if (login.profileCompleted){
                this.registrationStep = 1;
                }else{
                this.registrationStep = 2;
                }
            } else if (login.role.toLowerCase() === 'company') {
                this.currentCompany = login.username;
                if (!login.profileCompleted){
                    this.registrationStep = 2;
                }
                else{
                    if (login.approval_status === 'Pending'){
                        this.registrationStep = 3;
                        this.approval_status = login.approval_status
                    }else{
                        this.registrationStep = 1;
                        this.approval_status = login.approval_status
                    }
                }
            }
        },
        go_loginpage(role){
            this.isLoggedIn = false;
            this.showRegister = false;
            this.userRole = "";
            this.currentCompany = "";
            this.currentStudent = "";
            this.registrationStep = 1;
        }
    }
}
</script>
