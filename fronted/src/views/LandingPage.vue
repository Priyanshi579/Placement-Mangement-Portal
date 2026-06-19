<template>
    <div class = "main"> 
        <div>
            <h1 style = "text-align: center;">Placement Management Application</h1>
            <h2 style = "text-align: center;">Welcome to Placement Management Application</h2>
            <h4 style = "text-align: center;">Connect Students, Companies and Admins</h4>

        </div><br><br>
        <div>
            <button class="btn btn-outline-warning" @click = "$router.push('/admin')"> If you a Admin then click here for Admin View</button>
        </div><br><br>
        <div>
            <button class="btn btn-outline-warning" @click = "$router.push('/user')">If you a Student or company  then click here User View </button>
        </div>
    </div>
</template>

<script>
    export default{
        name:'LandingView'
    }
</script>

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