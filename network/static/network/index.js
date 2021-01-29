document.addEventListener('DOMContentLoaded', () =>
{
   const likeButton = document.querySelectorAll('.like-button');
   const editButton = document.querySelectorAll('.edit-button');
   const deleteButton = document.querySelectorAll('.delete-button');

   likeButton.forEach(button =>
   {
      hasLiked(button);

      button.onclick = (event) =>
      {
         const target = event.target;

         fetch(likeURL, {
            method: 'PUT',
            headers: {'X-CSRFToken': csrf_token},
            body: JSON.stringify({
               postID: target.dataset.id
            })
         })
             .then(response => response.json())
             .then(data => {
                target.innerHTML = data.likes;
                hasLiked(target);
             });
      }
   });

   editButton.forEach(button =>
   {
      button.onclick = (event) =>
      {
         const target = event.target;
         const col = target.parentElement.parentElement;

         col.style.display = 'none';

         const form = document.createElement('form');
         form.classList.add('w-100', 'p-3');
         form.style.display = 'block';

         const formGroup1 = document.createElement('div');
         formGroup1.classList.add('form-group');

         const formGroup2 = document.createElement('div');
         formGroup2.classList.add('form-group', 'm-0');

         const textarea = document.createElement('textarea');
         textarea.rows = 4;
         textarea.classList.add('form-control', 'w-100');
         textarea.value = col.parentNode.querySelector('.post-body').innerText;

         const submit = document.createElement('input');
         submit.type = 'submit';
         submit.value = 'Save';
         submit.classList.add('btn', 'btn-primary', 'w-100');

         const br = document.createElement('br');

         const h4 = document.createElement('h3');
         h4.innerText = 'Edit your post:';
         h4.classList.add('mb-2');
         h4.style.marginTop = '-10px';

         form.appendChild(h4);
         formGroup1.appendChild(textarea);
         form.appendChild(formGroup1);
         formGroup2.appendChild(submit);
         form.appendChild(formGroup2);
         form.appendChild(br);
         col.parentNode.appendChild(form);

         form.onsubmit = () => {
            fetch(editURL, {
               method: 'POST',
               headers: {'X-CSRFToken': csrf_token},
               body: JSON.stringify({
                  postID: target.dataset.id,
                  newText: textarea.value
               })
            })
                .then(() => {
                   form.style.display = 'none';
                   col.querySelector('.post-body').innerText = textarea.value;
                   form.style.display = 'block';
                });

            event.preventDefault();
         }
      }
   });

   deleteButton.forEach(button =>
   {
      button.onclick = (event) =>
      {
         const target = event.target;

         fetch(deleteURL, {
               method: 'POST',
               headers: {'X-CSRFToken': csrf_token},
               body: JSON.stringify({
                  postID: target.dataset.id
               })
            })
                .then(() => {
                   target.parentElement.parentElement.parentElement.style.height = '0';
                   target.parentElement.parentElement.parentElement.style.display = 'none';
                });
      }
   });
});

hasLiked = function(button)
{
   fetch(likedURL, {
      method: 'POST',
      headers: {'X-CSRFToken': csrf_token},
      body: JSON.stringify({
         postID: button.dataset.id
      })
   })
       .then(response => response.json())
       .then(data =>
       {
          if (data.status === 0)
          {
             button.classList.remove('fa', 'fa-heart');
             button.classList.add('fa', 'fa-heart-o');
          }
          else if (data.status === 1)
          {
             button.classList.remove('fa', 'fa-heart-o');
             button.classList.add('fa', 'fa-heart');
          }
       });
}