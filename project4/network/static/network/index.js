document.addEventListener("DOMContentLoaded", function() {
    // Check if the profile link was clicked
    const profileLink = document.querySelector("#profile_link");
    if (profileLink) {
        profileLink.addEventListener("click", function() {
            renderProfile();
        });
    }
    // Check if the all posts link was clicked
    const allPostLink = document.querySelector("#all_post_link");
    if (allPostLink) {
        allPostLink.addEventListener("click", function(event) {
            event.preventDefault();
            handleAllPostsClick();
        });
    }
    // Check if the followers link was clicked
    const followingLink = document.querySelector("#following_link");
    if (followingLink) {
        followingLink.addEventListener("click", function(event) {
            event.preventDefault();
            handleFollowingClick();
        });
    }
    // Check if the add post link was clicked
    const addLink = document.querySelector("#add_link");
    if (addLink) {
        addLink.addEventListener("click", function(event) {
            event.preventDefault();
            handleAddPostClick();
        });
    }
    // Check if the submit button was clicked
    const postSubmit = document.querySelector("#post_submit");
    if (postSubmit) {
        postSubmit.addEventListener("click", function(event) {
            event.preventDefault();
            handleSubmitPost();
        });

    }
    // check if the Search button was clicked or Enter key was pressed
    const searchBtn = document.getElementById("search-btn");
    const searchInput = document.getElementById("search-input");
    if (searchBtn && searchInput) {
        searchBtn.addEventListener("click", function() {
            const query = searchInput.value.trim();
            if (!query) return;
            handleSearch(query);
        });
        searchInput.addEventListener("keydown", function(e) {
            if (e.key === "Enter") {
                searchBtn.click();
            }
        });
    }
});

// Function to handle navigation (clicking back/forward buttons)
window.onpopstate = function(event) {
    const currentURL = window.location.pathname;
    if (event.state) {
        // User profile (with or without username)
        if (currentURL.startsWith("/profile/")) {
            // Followers
            if (currentURL.endsWith("/followers")) {
                const username = currentURL
                    .split("/profile/")[1]
                    .replace("/followers", "");
                showFollowers(username);
            }
            // Following
            else if (currentURL.endsWith("/following")) {
                const username = currentURL
                    .split("/profile/")[1]
                    .replace("/following", "");
                showFollowing(username);
            }
            // User comments
            else if (currentURL.endsWith("/comments")) {
                const username = currentURL
                    .split("/profile/")[1]
                    .replace("/comments", "");
                showUserComments(username);
            }
            // User likes
            else if (currentURL.endsWith("/likes")) {
                const username = currentURL.split("/profile/")[1].replace("/likes", "");
                showUserLikes(username);
            }
            // Default: user profile
            else {
                const username = currentURL.split("/profile/")[1];
                renderProfile(username || null);
            }
        } else if (currentURL === "/profile") {
            renderProfile();
        } else if (currentURL === "/add_post") { // Add post page
            showOnlySection("NewPost");
        } else if (currentURL === "/posts" || currentURL === "/") { // All posts page
            handleAllPostsClick();
        } else if (currentURL === "/following") {  // Following page
            handleFollowingClick();
        } else if (currentURL === "/followers") {
            showOnlySection("followers");
        } else if (currentURL.startsWith("/posts/")) {
            // Single post view
            const postId = currentURL.split("/posts/")[1];
            if (postId) {
                renderSinglePost(postId);
            } else {
                handleAllPostsClick();
            }
        }
    }
};
// Function to show only the specified section and hide others
function showOnlySection(sectionId) {
    const sections = [
        "profile",
        "NewPost",
        "posts",
        "following",
        "followers",
        "login_form",
        "register_form",
        "post",
        "all_posts",
        "search-results",
    ];

    sections.forEach((id) => {
        const el = document.querySelector(`.${id}`);
        if (el) {
            el.style.display = id === sectionId ? "block" : "none";
        }
    });
}

// Function to handle the click event for the add post link
function handleAddPostClick() {
    showOnlySection("NewPost");
    history.pushState({
        page: "add_post"
    }, "add_post", "/add_post");
    const postContentInput = document.querySelector("#post_content");
    if (postContentInput) {
        postContentInput.value = ""; // Clear the input field
    }
    //console.log("Add post link clicked, navigating to add post page.");
}

// Function to handle the click event for the following link
function handleSubmitPost() {
    // Validate the post content
    //console.log("Submit post button clicked.");
    const postContent = document.querySelector("#post_content").value;
    if (postContent.trim() === "") {
        alert("Post content cannot be empty.");
        return;
    }

    // Send the post content to the server
    fetch("/api/posts/", {
            method: "POST",
            credentials: "same-origin",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(), // Get CSRF token for security
            },
            body: JSON.stringify({
                content: postContent // Send the post content as JSON
            }),
        })
        .then((response) => {
            if (!response.ok) { 
                throw new Error("Network response was not ok"); 
            }
            return response.json();
        })
        .then((data) => {
            //console.log("Post submitted successfully:", data);
            handleAllPostsClick();
        })
        .catch((error) => {
            alert("There was a problem with the post submission: " + error.message);
            console.error("Error submitting post:", error);
        });
}

// Function to handle the click event for the all posts link
function handleAllPostsClick(page = 1) {
    showOnlySection("posts");
    renderPosts({
        apiUrl: "/api/posts/",
        containerSelector: ".posts",
        page,
        title: "All Posts",
        pushState: true,
        stateObj: {
            page: "posts"
        },
        urlPath: "/posts",
    });
}

// Function that renders all posts in the specified container
// It takes an object with the following properties:
function renderPosts({
    apiUrl,
    containerSelector,
    page = 1,
    title = "Posts",
    pushState = true,
    stateObj = {},
    urlPath = "",
}) {
    //push history state
    history.pushState({...stateObj,
            page_num: page
        },
        title.toLowerCase(),
        `${urlPath}?page=${page}`,
    );

    // Fetch posts from the API
    fetch(`${apiUrl}?page=${page}`, {
            method: "GET",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
        })
        .then((response) => {  // Check if the response is ok (status in the range 200-299)
            // If the response is not ok, throw an error
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then((data) => {
                if (pushState) {
                    history.pushState({...stateObj,
                            page_num: page
                        },
                        title.toLowerCase(),
                        `${urlPath}?page=${page}`,
                    );
                }

                const posts_content = document.createElement("div"); 
                posts_content.innerHTML = `
        <h1>${title}</h1>
        ${
          data.posts.length === 0
            ? `<div class="alert alert-info text-center my-4">No posts to display.</div>`
            : data.posts
                .map(
                  (post) => `
                <div class="post-card" data-post-id="${post.id}" style="cursor:pointer;">
                  <div class="post-header">
                    <a href="#" class="user-link" data-username="${post.user}">${post.user}</a>
                  </div>
                  <div class="post-meta">${timeAgo(post.created_at)} (${post.created_at})  </div>
                  <div class="post-content">${post.content}</div>
                  <div class="post-footer">
                    <span>Likes: <span class="like-count">${post.likes_count}</span></span>
                    <button class="like-btn btn btn-sm ${post.is_liked ? "btn-danger" : "btn-outline-primary"}">
                      ${post.is_liked ? "Unlike" : "Like"}
                    </button>
                  </div>
                </div>
              `,
                )
                .join("")
        }
        <div class="pagination">
          <button id="prev-page" ${!data.has_previous ? "disabled" : ""}>Previous</button>
          <button id="next-page" ${!data.has_next ? "disabled" : ""}>Next</button>
        </div>
      `;
      // Find the container where posts should be rendered
      // and replace its content with the new posts
      const postsContainer = document.querySelector(containerSelector);
      if (postsContainer) {
        postsContainer.innerHTML = "";
        postsContainer.appendChild(posts_content);

        // Like/Unlike event listeners
        posts_content.querySelectorAll(".like-btn").forEach((btn) => {
          btn.addEventListener("click", function () {
            if (window.userIsAuthenticated !== "true") {
              alert("You must be signed in to like posts.");
              return;
            }

            const postCard = this.closest(".post-card");
            const postId = postCard.getAttribute("data-post-id");
            const likeCountSpan = postCard.querySelector(".like-count");
            const isLiked = this.textContent === "Unlike";
            // Send like/unlike request to the server
            // Use fetch API to send a POST request to the server
            fetch(`/api/posts/${postId}/like/`, {
              method: isLiked ? "DELETE" : "POST",
              credentials: "same-origin",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
              },
            })
              .then((response) => response.json())
              .then((data) => {
                likeCountSpan.textContent = data.likes_count;
                this.textContent = data.is_liked ? "Unlike" : "Like";
                this.className = `like-btn btn btn-sm ${data.is_liked ? "btn-danger" : "btn-outline-primary"}`;
              })
              .catch((error) => {
                console.error(
                  "There was a problem with the like/unlike operation:",
                  error,
                );
              });
          });
        });
        addUserLinkListeners(); // Add user link listeners to the posts
        // Pagination handlers
        posts_content.querySelector("#prev-page").onclick = function () {
          if (data.has_previous)
            renderPosts({
              apiUrl,
              containerSelector,
              page: page - 1,
              title,
              pushState,
              stateObj,
              urlPath,
            });
        };
        posts_content.querySelector("#next-page").onclick = function () {
          if (data.has_next)
            renderPosts({
              apiUrl,
              containerSelector,
              page: page + 1,
              title,
              pushState,
              stateObj,
              urlPath,
            });
        };

          // Add click event to each post card to view single post
        // This will allow users to click on a post card to view the full post
          posts_content.querySelectorAll(".post-card").forEach((card) => {
          card.addEventListener("click", function (e) {
            // Prevent like button or user-link from triggering post view
            if (
              e.target.classList.contains("like-btn") ||
              e.target.classList.contains("user-link") ||
              e.target.closest(".user-link")
            ) return;
            const postId = this.getAttribute("data-post-id");
            renderSinglePost(postId);
          });
        });
      } else {
        console.error("Posts container not found.");
      }
    })
    .catch((error) => {
      alert("There was a problem with the fetch operation: " + error.message);
    });
}

// Function that reders profile of a user
// If username is provided, it will render that user's profile
// If no username is provided, it will render the current user's profile
// It also updates the browser history state to allow navigation back to this profile
function renderProfile(username = null) {
  showOnlySection("profile");
  let url, pushStateObj, pushUrl;
  if (username) {
    url = `/api/profile/${username}/`;
    pushStateObj = { page: "profile", username };
    pushUrl = `/profile/${username}`;
  } else {
    url = "/api/profile/";
    pushStateObj = { page: "profile" };
    pushUrl = "/profile";
  }
  //push history state
  // This will update the URL in the browser without reloading the page
  // and allow the user to navigate back to this state.
  history.pushState(pushStateObj, "profile", pushUrl);
  // Fetch profile data
  fetch(url)
    .then((response) => {
      if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
    })
    .then((data) => {
      document.querySelector(".profile").innerHTML = "";
      history.pushState(pushStateObj, "profile", pushUrl);

      const profile_content = document.createElement("div");
      profile_content.innerHTML = `
        <h1>${data.username}</h1>
        <p>
          <span id="followers-link" style="cursor:pointer; color:#007bff; text-decoration:underline;">
            Followers: ${data.followers}
          </span>
          &nbsp;|&nbsp;
          <span id="following-link" style="cursor:pointer; color:#007bff; text-decoration:underline;">
            Following: ${data.following}
          </span>
        </p>
        ${window.userIsAuthenticated === "true" && username ? 
          `<button id="follow-btn">${data.is_following ? "Unfollow" : "Follow"}</button>` 
          : ""
        }
       
        <div class="profile-posts"></div>
        ${
          !username
            ? `
        <h3>Maybe you want to Follow:</h3>
        <ul>
          ${data.random_users
            .map(
              (u) =>
                `<li><a href="#" class="user-link" data-username="${u}">${u}</a></li>`,
            )
            .join("")}
        </ul>
        `
            : ""
        }
        <div style="margin-top:20px;">
          <a href="#" id="show-user-comments" style="margin-right:20px; color:#007bff; text-decoration:underline;">All Comments</a>
          <a href="#" id="show-user-likes" style="color:#007bff; text-decoration:underline;">All Likes</a>
        </div>
      `;

      document.querySelector(".profile").append(profile_content);
      renderPosts({
          apiUrl: `/api/profile/${data.username}/posts/`,
          containerSelector: ".profile-posts",
          page: 1,
          title: `${data.username}'s Posts`,
          pushState: false
      });
      // Only show follow/unfollow for other users
      if (username && window.userIsAuthenticated === "true") {
        const followBtn = document.getElementById("follow-btn");
        if (data.is_their_profile) {
          followBtn.style.display = "none";
        } else {
          followBtn.style.display = "block";
          let isFollowing = data.is_following;
          followBtn.onclick = function () {
            fetch(`/api/profile/${username}/`, {
              method: isFollowing ? "DELETE" : "POST",
              credentials: "same-origin",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
              },
            })
              .then((response) => response.json())
              .then((response) => {
                renderProfile(username);
              })
              .catch((error) => {
                console.error(
                  "There was a problem with the follow/unfollow operation:",
                  error,
                );
              });
          };
        }
      }
      // Add event listeners for user links (only on own profile)
      if (!username) {
        addUserLinkListeners(document.querySelector(".profile"));
      }
      // Followers link
      const followersLink = document.getElementById("followers-link");
      if (followersLink) {
        followersLink.addEventListener("click", function () {
        showFollowers(data.username);
        });
      }
      // Following link
      const followingLink = document.getElementById("following-link");
      if (followingLink) {
        followingLink.addEventListener("click", function () {
          showFollowing(data.username);
        });
      }
      // Add event listeners for user comments and likes
      const showUserCommentsBtn = document.getElementById("show-user-comments");
      if (showUserCommentsBtn) {
        showUserCommentsBtn.addEventListener("click", function (e) {
          e.preventDefault();
          showUserComments(data.username); // Now this refers to the function!
        });
      }
      // Show user likes
      const showUserLikesBtn = document.getElementById("show-user-likes");
      if (showUserLikesBtn) {
        showUserLikesBtn.addEventListener("click", function (e) {
          e.preventDefault();
          showUserLikes(data.username);
        });
      }
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
}

// Function to show following page (posts of users that the current user is following)
function handleFollowingClick(page = 1) {
  showOnlySection("following");
  renderPosts({
    apiUrl: "/api/following/",
    containerSelector: ".following",
    page,
    title: "Following's Posts",
    pushState: true,
    stateObj: { page: "following" },
    urlPath: "/following",
  });
}

// Function to handle CSRF token retrieval
// This function retrieves the CSRF token from cookies
function getCSRFToken() {
  const name = "csrftoken";
  const cookies = document.cookie.split(";");
  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name + "=")) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null;
}

// Function to render single post by its ID
// This function fetches the post and its comments, then displays them
function renderSinglePost(postId) {
  showOnlySection("posts");
  history.pushState(
    { page: "single_post", postId },
    "post",
    `/posts/${postId}`,
  );

  // Fetch post and comments in parallel
  Promise.all([
    fetch(`/api/posts/${postId}/`, {
      method: "GET",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
    }).then((response) => response.json()),
    fetch(`/api/posts/${postId}/comment/`).then((response) => response.json())
  ]).then(([post, commentData]) => {
    const postsContainer = document.querySelector(".posts");
    const commentsHtml = commentData.comments
      .map(
        (c) => `
      <div class="comment">
        <strong  class="user-link" data-username="${c.user}">${c.user}</strong>: ${c.content}
        <span class="comment-date">${timeAgo(c.created_at)}</span>
      </div>
    `
      )
      .join("");

    postsContainer.innerHTML = `
      <div class="post-card" data-post-id="${post.id}">
        <div class="post-header">
          <a href="#" class="user-link" data-username="${post.user}">${post.user}</a>
        </div>
        <div class="post-meta">${timeAgo(post.created_at)} (${post.created_at})  </div>
        <div class="post-content" id="post-content">${post.content}</div>
        <div class="post-footer">
          <span>Likes: <span class="like-count">${post.likes_count}</span></span>
          ${
            post.can_like
              ? `
            <button class="like-btn btn btn-sm ${post.is_liked ? "btn-danger" : "btn-outline-primary"}">
              ${post.is_liked ? "Unlike" : "Like"}
            </button>
          `
              : ""
          }
          ${
            post.can_edit
              ? `
            <button class="edit-btn btn btn-sm btn-warning">Edit</button>
          `
              : ""
          }
        </div>
        <div class="comments-section">
          <h4>Comments</h4>
          <div id="comments-list">${commentsHtml}</div>
          ${
            window.userIsAuthenticated === "true"
              ? `
            <textarea id="new-comment-content" class="form-control" placeholder="Add a comment"></textarea>
            <button id="submit-comment" class="btn btn-primary btn-sm mt-2">Post Comment</button>
          `
              : `<div class="text-muted">Sign in to comment.</div>`
          }
        </div>
      </div>
    `;
    // Add user link listeners
    addUserLinkListeners(postsContainer);
    // Like/Unlike handler
    const likeBtn = postsContainer.querySelector(".like-btn");
    if (likeBtn) {
      likeBtn.addEventListener("click", function () {
        if (window.userIsAuthenticated !== "true") {
          alert("You must be signed in to like posts.");
          return;
        }
        fetch(`/api/posts/${post.id}/like/`, {
          method: post.is_liked ? "DELETE" : "POST",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
        })
          .then((response) => response.json())
          .then((data) => {
            postsContainer.querySelector(".like-count").textContent =
              data.likes_count;
            likeBtn.textContent = data.is_liked ? "Unlike" : "Like";
            likeBtn.className = `like-btn btn btn-sm ${data.is_liked ? "btn-danger" : "btn-outline-primary"}`;
            post.is_liked = data.is_liked; // update local state
          });
      });
    }
    const editBtn = postsContainer.querySelector(".edit-btn");
    if (editBtn) {
      editBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      if (postsContainer.querySelector("#edit-content")) return;
      const contentDiv = postsContainer.querySelector("#post-content");
      const oldContent = contentDiv.textContent;
      editBtn.style.display = "none";
      contentDiv.innerHTML = `
        <textarea id="edit-content" class="form-control">${oldContent}</textarea>
        <div style="margin-top:8px;">
          <button id="save-edit" class="btn btn-success btn-sm mt-2">Save</button>
          <button id="cancel-edit" class="btn btn-secondary btn-sm mt-2">Cancel</button>
        </div>
      `;
      contentDiv.className = "edit-content";
      document.getElementById("save-edit").onclick = function () {
      const newContent = document.getElementById("edit-content").value;
      fetch(`/api/posts/${postId}/`, {
        method: "PUT",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ content: newContent }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            alert(data.error); // Show the backend error
            return;
          }
          renderSinglePost(postId); // Only re-render if no error
        })
        .catch((error) => {
          alert("There was a problem saving your edit: " + error.message);
          contentDiv.innerHTML = oldContent;
          contentDiv.id = "post-content";
          contentDiv.className = "post-content";
          editBtn.style.display = "";
        });
    };

      document.getElementById("cancel-edit").onclick = function () {
        contentDiv.innerHTML = oldContent;
        contentDiv.id = "post-content";
        contentDiv.className = "post-content";
        editBtn.style.display = "";
      };
    });
  }
    // Comment submit handler
    if (window.userIsAuthenticated === "true") {
      const submitCommentBtn = document.getElementById("submit-comment");
      if (submitCommentBtn) {
        submitCommentBtn.onclick = function () {
          const content = document.getElementById("new-comment-content").value.trim();
          if (!content) return;
          fetch(`/api/posts/${post.id}/comment/`, {
            method: "POST",
            credentials: "same-origin",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ content }),
          })
            .then((response) => response.json())
            .then((newComment) => {
              // Add new comment to the list
              const commentDiv = document.createElement("div");
              commentDiv.className = "comment";
              commentDiv.innerHTML = `<strong>${newComment.user}</strong>: ${newComment.content} <span class="comment-date">${newComment.created_at}</span>`;
              document.getElementById("comments-list").appendChild(commentDiv);
              document.getElementById("new-comment-content").value = "";
            });
        };
      }
    }
  });
}

// Function to show followers of a user
// This function fetches the followers of a user and displays them
function showFollowers(username) {
  //push history state for followers
  history.pushState(
    { page: "followers", username },
    `${username}'s Followers`,
    `/profile/${username}/followers`,
  );
  // Show followers section
  showOnlySection("followers");
  fetch(`/api/profile/${username}/`, {
    method: "GET",
    credentials: "same-origin",
  })
    .then((response) => response.json())
    .then((data) => {
      const followersList = data.followers_list;
      document.querySelector(".followers").innerHTML = `
        <h2>${username}'s Followers</h2>
        ${
          followersList.length === 0
            ? `<div class="alert alert-info text-center my-4">No followers yet.</div>`
            : `<ul>
                ${followersList.map((u) => `<li><a href="#" class="user-link" data-username="${u}">${u}</a></li>`).join("")}
              </ul>`
        }
      `;
      addUserLinkListeners(document.querySelector(".followers"));
    });
}

// Function to show following users of a user
// This function fetches the users that a user is following and displays them
function showFollowing(username) {
  //push history state for following
  history.pushState(
    { page: "following", username },
    `${username} is Following`,
    `/profile/${username}/following`,
  );
  showOnlySection("following");
  fetch(`/api/profile/${username}/`, {
    method: "GET",
    credentials: "same-origin",
  })
    .then((response) => response.json())
    .then((data) => {
      document.querySelector(".following").innerHTML = `
      <h2>${username} is Following</h2>
      <ul>
        ${
          data.following_list.length === 0
            ? `<div class="alert alert-info text-center my-4">Not following anyone yet.</div>`
            : `<ul>
          ${data.following_list.map((u) => `<li><a href="#" class="user-link" data-username="${u}">${u}</a></li>`).join("")}     
      </ul>`
        }
    `;
      addUserLinkListeners(document.querySelector(".following"));
    });
}

// Function to show comments made by a user
// This function fetches the comments made by a user and displays them
// It also allows users to click on a post link to view the full post
function showUserComments(username) {
  showOnlySection("posts");
  history.pushState(
    { page: "comments", username },
    `${username}'s Comments`,
    `/profile/${username}/comments`,
  );
  fetch(`/api/profile/${username}/comments/`)
    .then((response) => response.json())
    .then((data) => {
      document.querySelector(".posts").innerHTML = `
        <h2>${username}'s Comments</h2>
        ${
          data.comments.length === 0
            ? `<div class="alert alert-info text-center my-4">No comments to display.</div>`
            : `<ul>
                ${data.comments
                  .map(
                    (c) => `
                      <li>
                        <strong>${c.user}</strong> 
                        <a href="#" class="post-link" data-post-id="${c.post}">
                          ${c.content}
                        </a>
                        <br>
                        "${c.content}"
                      </li>
                    `
                  )
                  .join("")}
              </ul>`
        }
      `;
      // Add event listeners to post links
      document.querySelectorAll(".post-link").forEach(link => {
        link.addEventListener("click", function(e) {
          e.preventDefault();
          renderSinglePost(this.dataset.postId);
        });
      });
    });
}


// Function to show likes made by a user
// This function fetches the likes made by a user and displays them
// It also allows users to click on a post link to view the full post
function showUserLikes(username) {
  showOnlySection("posts");
  history.pushState(
    { page: "likes", username },
    `${username}'s Likes`,
    `/profile/${username}/likes`,
  );
  fetch(`/api/profile/${username}/likes/`)
    .then((response) => response.json())
    .then((data) => {
      document.querySelector(".posts").innerHTML = `
        <h2>${username}'s Likes</h2>
        ${
          data.likes.length === 0
            ? `<div class="alert alert-info text-center my-4">No liked posts to display.</div>`
            : `<ul>
                ${data.likes
                  .map(
                    (like) => `
                      <li>
                        Liked post by <strong>${like.user}</strong>:
                        <a href="#" class="post-link" data-post-id="${like.post_id}">
                          ${like.post_content}
                        </a>
                      </li>
                    `
                  )
                  .join("")}
              </ul>`
        }
      `;
      // Add event listeners to post links
      document.querySelectorAll(".post-link").forEach(link => {
        link.addEventListener("click", function(e) {
          e.preventDefault();
          renderSinglePost(this.dataset.postId);
        });
      });
    });
}

// Function to add click event listeners to user links
// Renders the user's profile when a user link is clicked
function addUserLinkListeners(scope = document) {
  // Add click event listeners to user links within the specified scope
  scope.querySelectorAll(".user-link").forEach(link => {
    link.addEventListener("click", function(e) {
      e.preventDefault();
      renderProfile(this.dataset.username);
    });
  });
}

// Function to handle search functionality
function handleSearch(query) {
  //push history state for search
  history.pushState(
    { page: "search", query },
    `Search results for "${query}"`,
    `/search?q=${encodeURIComponent(query)}`,
  );
  // Show search results section
  showOnlySection("search-results");
  if (!query) return;
  fetch(`/api/search/?q=${encodeURIComponent(query)}`, {
    method: "GET",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    }, 
  })
    .then((response) => {
      if (!response.ok) throw new Error("Network response was not ok");
      return response.json();
    })
    .then((data) => { 
      const resultsContainer = document.querySelector(".search-results");
      if (!resultsContainer) {
        console.error("Search results container not found.");
        return;
      }
      resultsContainer.innerHTML = ""; // Clear previous results
            const hasUsers = data.users && data.users.length > 0;
      const hasPosts = data.posts && data.posts.length > 0;
      
      if (!hasUsers && !hasPosts) {
        resultsContainer.innerHTML = `<div class="alert alert-info text-center my-4">No results found for "${query}".</div>`;
        return;
      }
      
      // Show users
      if (hasUsers) {
        resultsContainer.innerHTML += `<h4>Users</h4>`;
        data.users.forEach((user) => {
          resultsContainer.innerHTML += `
            <div class="search-result">
              <a href="#" class="user-link" data-username="${user.username}">${user.username}</a>
            </div>
          `;
        });
      }
      
            if (hasPosts) {
        resultsContainer.innerHTML += `<h4>Posts</h4>`;
        data.posts.forEach((post) => {
          resultsContainer.innerHTML += `
            <div class="search-result">
              <a href="#" class="post-link" data-post-id="${post.id}">
                ${post.content}
              </a>
              <p>by <span class="user-link" data-username="${post.user}">${post.user}</span></p>
            </div>
          `;
        });
        // Add click event listeners to post links
        resultsContainer.querySelectorAll(".post-link").forEach(link => {
          link.addEventListener("click", function(e) {
            e.preventDefault();
            renderSinglePost(this.dataset.postId);
          });
        });
      }
      
      // Add user link listeners
      addUserLinkListeners(resultsContainer);
     
    })
    .catch((error) => {
      console.error("There was a problem with the search operation:", error);
      alert("There was a problem with the search operation: " + error.message);
    } );
}


// Function to calculate time ago from a date string
// This function takes a date string and returns a human-readable time ago format
function timeAgo(dateString) {
  const now = new Date();
  const date = new Date(dateString);
  const seconds = Math.floor((now - date) / 1000);

  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} minute${minutes !== 1 ? "s" : ""} ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} hour${hours !== 1 ? "s" : ""} ago`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days} day${days !== 1 ? "s" : ""} ago`;
  const weeks = Math.floor(days / 7);
  if (weeks < 4) return `${weeks} week${weeks !== 1 ? "s" : ""} ago`;
  const months = Math.floor(days / 30);
  if (months < 12) return `${months} month${months !== 1 ? "s" : ""} ago`;
  const years = Math.floor(days / 365);
  return `${years} year${years !== 1 ? "s" : ""} ago`;
}