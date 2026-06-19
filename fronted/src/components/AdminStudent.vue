<template>
    <div>
        <h1 style = "text-align: center;">List of registered Students</h1>
        <div class = "table" style = "text-align: center;">
            <table border = "10px" bordlinecolor="white">
                <thead>
                    <tr>
                        <td>Name</td>
                        <td>Email</td>
                        <td>Phone</td>
                        <td>Branch</td>
                        <td>Year</td>
                        <td>CGPA</td>
                        <td>Skills</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for = "student in student_details" :key = "student.id">
                        <td>{{student.name}} </td>
                        <td>{{student.email}} </td>
                        <td>{{student.phone}} </td>
                        <td>{{student.branch}} </td>
                        <td>{{student.year}} </td>
                        <td>{{student.cgpa}} </td>
                        <td>{{student.skills}} </td>
                        <td> <button class="btn btn-danger" @click="blacklisted_student(student.id)">Blacklist</button></td>
                    </tr>
                </tbody>

            </table>
        </div>
    </div>
    
</template>
<script>
import axios from 'axios'
export default{
    name:'AdminStudent',
    data(){
        return{
            student_details:[]
        }
    },
    methods:{
        async fetchstudentdetails(){
            const token = localStorage.getItem('admin_token');
            const res = await axios.get('http://localhost:5000/api/get/student',{
                headers:{
                    Authorization: `Bearer ${token}`
                }
            });
            this.student_details = res.data
            
        },
        async blacklisted_student(id){
            const token = localStorage.getItem('admin_token')
            const res = await axios.post(`http://localhost:5000/api/blacklisted_student/${id}`,{},{
                headers:{
                    Authorization:`Bearer ${token}`
                }
            })
            this.student_details = this.student_details.filter(student => Number(student.id) !== Number(id))
            alert("student is blacklisted successful")

        }
        

    },
    mounted(){
        this.fetchstudentdetails()
    }
}
</script>
<style scoped>
    .table{
        border:none;
        margin-top:10px;
        width:715px;
        /* ADD THESE THREE LINES TO CENTER THE CANVAS: */
        display: flex;
        justify-content: center; /* Centers horizontally */
        align-items: flex-start; /* Keeps the canvas layout sticking towards the top */
        /* min-height: 100vh; */
    }
</style>