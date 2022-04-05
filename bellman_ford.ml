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


let bellman_ford g vi =
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
  let distance = Array.make n Infini in
  distance.(vi)<-Entier(0);
  for k=0 to (n-1) do
    for i=0 to n-1 do
      let mini = ref Infini in
      for j=0 to n-1 do
        mini:=opt (!mini) (somme distance.(j) g.(j).(i))
      done;
      distance.(i)<-opt distance.(i) (!mini) 
    done;
  done;
  distance
;;

