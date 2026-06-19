import { createRouter,createWebHistory } from "vue-router"; 
import LandingPage from '../views/LandingPage.vue'
import AdminView from '../views/AdminView.vue'    
import UserView from '../views/UserView.vue'
import CreateDrive from '../components/CreateDrive.vue'
import StudentrRegister from '../components/StudentRegister.vue'
import CompanyDrives from '../components/CompanyDrives.vue'
import DriveDetails from '../components/DriveDetails.vue'
import CompanyDashboard from '../components/CompanyDashboard.vue'
import StudentDashboard from '../components/StudentDashboard.vue'
import StudentDetails from '../components/StudentDetails.vue'
import HistoryView from '../components/HistoryView.vue'
import UpdateApplication from '../components/UpdateApplication.vue'
import StudentData from '../components/StudentData.vue'
import SearchBar from '../components/SearchBar.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import UpdateDrive from '../components/UpdateDrive.vue'
import DriveAppliedDetails from '../components/DriveAppliedDetails.vue'
import AdminDriveDet from '../components/AdminDriveDet.vue'
const routes = [{path: '/',component:LandingPage},
    {path: '/admin',component:AdminView},
    {path:'/admin/dashboard',name:'AdminDashboard',component:AdminDashboard},
    {path: '/user',name: 'UserDashboard', component:UserView},
    {path:'/create_drive', component:CreateDrive},
    {path:'/update_student',component:StudentrRegister},
    {path:'/company/drives/:id', name: 'CompanyDrives', component:CompanyDrives},
    {path:'/drives/:id', name: 'DriveDetails', component:DriveDetails},
    {path:'/company/dashboard', name: 'CompanyDashboard', component:CompanyDashboard},
    {path:'/student/dashboard', name: 'StudentDashboard', component:StudentDashboard},
    {path:'/student_application/:id', name: 'StudentDetails', component:StudentDetails},
    {path: '/applied_history/:student_id', name: 'HistoryView', component:HistoryView},
    {path:'/update_drive/:drive_id', name: 'UpdateApplication', component:UpdateApplication},
    {path:'/studentdata/:student_id/:drive_id',name:'StudentData',component:StudentData},
    {path:'/search/:user_type/:search',name:'SearchBar',component:SearchBar},
    {path:'/update_drive/details/:drive_id',name:'UpdateDrive',component:UpdateDrive},
    {path:'/applied/drive/details/:drive_id',name:'AppliedDriveDetails',component:DriveAppliedDetails},
    {path:'/admin/drives/:drive_id',name:'AdminDriveDetails',component:AdminDriveDet},
    {path: '/:pathMatch(.*)*',redirect:'/'}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
