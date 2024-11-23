CREATE TABLE IF NOT EXISTS movies (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY ,
    title text,
    year int,
    ratings int,
    url text,

    created_at       bigint default date_part('epoch'::text, now()) not null,
    updated_at       bigint default date_part('epoch'::text, now()) not null
);

CREATE TABLE IF NOT EXISTS movie_actors (
    movie_id int,
    actor_name text,
    created_at       bigint default date_part('epoch'::text, now()) not null,
    updated_at       bigint default date_part('epoch'::text, now()) not null,

    primary key (movie_id, actor_name), -- treadted as unique to simplify the scope
    foreign key (movie_id) references movies (id) on delete cascade
);

CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id int,
    genre text,
    created_at       bigint default date_part('epoch'::text, now()) not null,
    updated_at       bigint default date_part('epoch'::text, now()) not null,

    primary key (movie_id, genre),
    foreign key (movie_id) references movies (id) on delete cascade
);
