type entier =
  | Infini
  | Entier of int;;

let w = [|[|Entier(0); Infini; Infini; Infini; Infini; Infini|];
          [|Entier(2); Entier(0); Infini; Infini; Entier(5); Infini|];
          [|Infini; Infini; Entier(0); Entier(7); Entier(1); Entier(2)|];
          [|Infini; Entier(1); Infini; Entier(0); Infini; Infini|];
          [|Infini; Entier(6); Infini; Entier(4); Entier(0); Infini|];
          [|Infini; Infini; Entier(3); Infini; Infini; Entier(0)|]
        |];;


let floyd_warshall g =
  let opt a b = match a,b with
    |Infini,Infini->Infini
    |Entier(x),Infini->a
    |Infini,Entier(y)->b
    |Entier(x),Entier(y)-> if x<y then a else b
  in
  let somme a b = match a,b with
    |Infini,_->Infini
    |_,Infini-> Infini
    |Entier(x), Entier(y)-> Entier(x+y)
  in
  let n = Array.length g in
  let m = Array.make_matrix n n Infini in
  for i=0 to n-1 do
    for j=0 to n-1 do
      m.(i).(j)<-g.(i).(j)
    done;
  done;
  for k=1 to n-1 do
    for i=0 to n-1 do
      for j=0 to n-1 do
        m.(i).(j)<-opt m.(i).(j) (somme m.(i).(k) m.(k).(j))
      done;
    done;
  done;
  m
;;

let floyd_warshall_avec_chemin g =
  let n = Array.length g in
  let m = Array.make_matrix n n Infini in
  let chemin = Array.make_matrix n n [] in
  let somme a b = match a,b with
    |Infini,_->Infini
    |_,Infini-> Infini
    |Entier(x), Entier(y)-> Entier(x+y)
  in
  let opt i j k = match m.(i).(j),(somme m.(i).(k) m.(k).(j)) with
    |Infini,Infini->Infini
    |Entier(x),Infini->m.(i).(j)
    |Infini,Entier(y)->
      begin
        chemin.(i).(j)<-(chemin.(i).(k))@(k::(chemin.(k).(j)));
        (somme m.(i).(k) m.(k).(j))
      end
    |Entier(x),Entier(y)-> if x<=y then m.(i).(j) else
                             begin
                               chemin.(i).(j)<-(chemin.(i).(k))@(k::(chemin.(k).(j)));
                               (somme m.(i).(k) m.(k).(j))
                             end
  in
  for i=0 to n-1 do
    for j=0 to n-1 do
      m.(i).(j)<-g.(i).(j);
    done;
  done;
  for k=1 to n-1 do
    for i=0 to n-1 do
      for j=0 to n-1 do
        m.(i).(j)<-opt i j k
      done;
    done;
  done;
  (m,chemin)
;;
    
