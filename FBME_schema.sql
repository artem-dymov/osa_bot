PGDMP     %    -            
    z            sova-dev-ubuntu     15.1 (Ubuntu 15.1-1.pgdg20.04+1)    15.0     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    24604    sova-dev-ubuntu    DATABASE     y   CREATE DATABASE "sova-dev-ubuntu" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C.UTF-8';
 !   DROP DATABASE "sova-dev-ubuntu";
                postgres    false                        2615    32879    FBME    SCHEMA        CREATE SCHEMA "FBME";
    DROP SCHEMA "FBME";
                postgres    false            �           0    0    SCHEMA "FBME"    COMMENT     6   COMMENT ON SCHEMA "FBME" IS 'standard public schema';
                   postgres    false    6            �            1259    32886    teachers    TABLE     �   CREATE TABLE "FBME".teachers (
    id integer NOT NULL,
    full_name text NOT NULL,
    type text DEFAULT 'NO DATA'::text NOT NULL,
    groups text[]
);
    DROP TABLE "FBME".teachers;
       FBME         heap    postgres    false    6            �            1259    32892    teachers_id_seq    SEQUENCE     �   CREATE SEQUENCE "FBME".teachers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE "FBME".teachers_id_seq;
       FBME          postgres    false    222    6                        0    0    teachers_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE "FBME".teachers_id_seq OWNED BY "FBME".teachers.id;
          FBME          postgres    false    223            �            1259    32885    votes_id_seq    SEQUENCE     �   CREATE SEQUENCE "FBME".votes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE "FBME".votes_id_seq;
       FBME          postgres    false    6            �            1259    32880    votes    TABLE     �   CREATE TABLE "FBME".votes (
    id integer DEFAULT nextval('"FBME".votes_id_seq'::regclass) NOT NULL,
    user_id integer,
    teacher_id integer,
    marks integer[],
    questions_id integer[]
);
    DROP TABLE "FBME".votes;
       FBME         heap    postgres    false    221    6            _           2604    32894    teachers id    DEFAULT     j   ALTER TABLE ONLY "FBME".teachers ALTER COLUMN id SET DEFAULT nextval('"FBME".teachers_id_seq'::regclass);
 :   ALTER TABLE "FBME".teachers ALTER COLUMN id DROP DEFAULT;
       FBME          postgres    false    223    222            �          0    32886    teachers 
   TABLE DATA           ?   COPY "FBME".teachers (id, full_name, type, groups) FROM stdin;
    FBME          postgres    false    222   F       �          0    32880    votes 
   TABLE DATA           M   COPY "FBME".votes (id, user_id, teacher_id, marks, questions_id) FROM stdin;
    FBME          postgres    false    220   �                  0    0    teachers_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('"FBME".teachers_id_seq', 5, true);
          FBME          postgres    false    223                       0    0    votes_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('"FBME".votes_id_seq', 7, true);
          FBME          postgres    false    221            b           2606    32896    votes poll_pkey 
   CONSTRAINT     M   ALTER TABLE ONLY "FBME".votes
    ADD CONSTRAINT poll_pkey PRIMARY KEY (id);
 9   ALTER TABLE ONLY "FBME".votes DROP CONSTRAINT poll_pkey;
       FBME            postgres    false    220            d           2606    32898    teachers teachers_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY "FBME".teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY "FBME".teachers DROP CONSTRAINT teachers_pkey;
       FBME            postgres    false    222            e           2606    32899    votes poll_teacher_id_fkey    FK CONSTRAINT        ALTER TABLE ONLY "FBME".votes
    ADD CONSTRAINT poll_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES "FBME".teachers(id);
 D   ALTER TABLE ONLY "FBME".votes DROP CONSTRAINT poll_teacher_id_fkey;
       FBME          postgres    false    222    220    3172            f           2606    32904    votes poll_user_id_fkey    FK CONSTRAINT     v   ALTER TABLE ONLY "FBME".votes
    ADD CONSTRAINT poll_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 A   ALTER TABLE ONLY "FBME".votes DROP CONSTRAINT poll_user_id_fkey;
       FBME          postgres    false    220            �   �   x�3�tJ�.�SpRp�,(JL.�LN�N*�54��2�0��.6_ثpa��1��f�\F�^�qa˅}.컰I�BHuNjrIi�b��Ɯ�\�va�Ş�.�+��j��I-�)�ea@�%�dpVC���L��@��B}|�Dm-W� �RI      �   i   x�M�A�0�𖍑�'�7o����Ң�ɲ3PH�P���
q�$(�*ԝ+� cA6g�&�tu���n�Ԥp��>��C kJ�������X��f��\-�     